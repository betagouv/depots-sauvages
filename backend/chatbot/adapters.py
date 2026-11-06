import json
import logging
import re
import time
import uuid
from typing import Any, Dict, Generator, List, Optional
import requests
from django.conf import settings
from backend.chatbot.context import scrub_pii
from backend.chatbot.models import ChatbotConfig, DEFAULT_SYSTEM_PROMPT
from backend.chatbot.retriever import get_retriever

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = DEFAULT_SYSTEM_PROMPT

TOOL_PROPOSE_CONSTATATION_DRAFT = {
    "type": "function",
    "function": {
        "name": "propose_constatation_draft",
        "description": "Propose à l'utilisateur de pré-remplir un brouillon de constatation sur Stop Dépôt Sauvage.",
        "parameters": {
            "type": "object",
            "properties": {
                "commune": {
                    "type": "string",
                    "description": "Nom de la commune concernée par le dépôt",
                },
                "localisationDepot": {
                    "type": "string",
                    "description": "Précision sur le lieu du dépôt (rue, chemin, lieu-dit, coordonnées)",
                },
                "volumeDepot": {
                    "type": "string",
                    "enum": [
                        "Moins de 1m3",
                        "Entre 1 et 3m3",
                        "Entre 3 et 10m3",
                        "Entre 10 et 100m3",
                        "Plus de 100m3",
                    ],
                    "description": "Fourchette de volume estimée du dépôt",
                },
                "volumeM3": {
                    "type": "number",
                    "description": "Volume chiffré estimé en m3 (ex: 0.5, 2.0, 5.0, 15.0)",
                },
                "typesDepot": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Types de déchets constatés (ex: Gravats, Encombrants, Pneus, Déchets verts, Amiante, etc.)",
                },
                "natureTerrain": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Nature du terrain : 'domaine public' ou 'propriété privée'",
                },
                "auteurIdentifie": {
                    "type": "boolean",
                    "description": "Si l'auteur du dépôt a été identifié ou soupçonné",
                },
                "precisionsDepot": {
                    "type": "string",
                    "description": "Remarques ou détails complémentaires relevés",
                },
            },
            "required": ["typesDepot"],
        },
    },
}


def sse_event(data: Dict[str, Any]) -> str:
    """Format dictionary as Server-Sent Event for Vercel AI SDK."""
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


def stream_text_words(text_id: str, full_text: str, delay: float = 0.045) -> Generator[str, None, None]:
    """Emit text word-by-word with delay to produce a natural streaming effect."""
    tokens = re.findall(r"\S+\s*|\n", full_text)
    for token in tokens:
        yield sse_event({"type": "text-delta", "id": text_id, "delta": token})
        if delay > 0:
            time.sleep(delay)


class BaseAIAdapter:
    def stream_chat(
        self, messages: List[Dict[str, Any]], context: Optional[Dict[str, Any]] = None
    ) -> Generator[str, None, None]:
        raise NotImplementedError


class MockAIAdapter(BaseAIAdapter):
    """Realistic mock adapter simulating regulatory advice and draft generation."""

    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode

    def stream_chat(
        self, messages: List[Dict[str, Any]], context: Optional[Dict[str, Any]] = None
    ) -> Generator[str, None, None]:
        text_id = f"txt_{uuid.uuid4().hex[:8]}"

        last_user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                content = msg.get("content", "")
                if isinstance(content, str):
                    last_user_message = content
                elif isinstance(tool_parts := msg.get("parts"), list):
                    last_user_message = " ".join(
                        p.get("text", "") for p in tool_parts if isinstance(p, dict)
                    )
                break

        query = last_user_message.lower()

        if self.debug_mode:
            logger.info(
                "\n==================== [CHATBOT AI DEBUG REQUEST (MOCK)] ====================\n"
                "Model          : mock-local-simulator\n"
                "Messages count : %d\n"
                "Last query     : %s\n"
                "Context        : %s\n"
                "==========================================================================",
                len(messages),
                last_user_message,
                json.dumps(context or {}, indent=2, ensure_ascii=False),
            )

        keywords_draft = [
            "gravat",
            "déchet",
            "dechet",
            "pneu",
            "brouillon",
            "constat",
            "encombrant",
            "amiante",
            "déposer",
            "deposer",
            "signalement",
        ]
        wants_draft = any(kw in query for kw in keywords_draft)

        yield sse_event({"type": "text-start", "id": text_id})

        if wants_draft:
            intro_text = (
                "J'ai bien pris note de ces éléments concernant le dépôt sauvage constaté. "
                "Conformément à la réglementation (Code de l'environnement, art. L. 541-3), "
                "une première constatation contradictoire sur le terrain est indispensable "
                "pour amorcer la procédure administrative ou pénale.\n\n"
                "Voici les éléments prêts pour votre dossier. Vous pouvez valider "
                "et créer votre brouillon de constatation ci-dessous :"
            )
            yield from stream_text_words(text_id, intro_text)
            yield sse_event({"type": "text-end", "id": text_id})

            types_depot = []
            if "gravat" in query:
                types_depot.append("Gravats")
            if "pneu" in query:
                types_depot.append("Pneus")
            if "amiante" in query:
                types_depot.append("Amiante")
            if "vert" in query:
                types_depot.append("Déchets verts")
            if not types_depot:
                types_depot = ["Encombrants"]

            volume = "Entre 1 et 3m3"
            volume_m3 = 2.0
            if "10" in query or "important" in query or "gros" in query:
                volume = "Entre 3 et 10m3"
                volume_m3 = 6.0
            elif "petit" in query or "sac" in query or "moins" in query:
                volume = "Moins de 1m3"
                volume_m3 = 0.5

            commune_match = re.search(r"(?:à|a|sur|commune de)\s+([A-ZÀ-Ÿ][a-zà-ÿ\-]+)", last_user_message)
            commune = commune_match.group(1) if commune_match else ""

            tool_call_id = f"call_{uuid.uuid4().hex[:10]}"
            tool_input = {
                "commune": commune,
                "localisationDepot": "Chemin rural / abords de voirie",
                "volumeDepot": volume,
                "volumeM3": volume_m3,
                "typesDepot": types_depot,
                "natureTerrain": ["domaine public"],
                "auteurIdentifie": False,
                "precisionsDepot": f"Signalé via l'assistant contextuel : {last_user_message.strip()}",
            }

            yield sse_event(
                {
                    "type": "tool-input-available",
                    "toolCallId": tool_call_id,
                    "toolName": "propose_constatation_draft",
                    "input": tool_input,
                }
            )

        elif "délai" in query or "delai" in query or "procédure" in query or "procedure" in query:
            text = (
                "Pour les dépôts sauvages, deux voies de procédure sont mobilisables par le maire ou l'agent assermenté :\n\n"
                "1. **Voie administrative (L. 541-3 C. Env.)** :\n"
                "- Transmission d'une mise en demeure avec un délai contradictoire (généralement 10 jours ouvrés pour formuler des observations).\n"
                "- Si le dépôt n'est pas évacué : arrêté d'astreinte journalière (jusqu'à 1500 €/jour) ou amende administrative (jusqu'à 15 000 €).\n\n"
                "2. **Voie pénale (R. 635-8 du Code pénal)** :\n"
                "- Rédaction d'un Procès-Verbal d'infraction, transmis au Procureur de la République dans les 5 jours de sa clôture.\n\n"
                "Avez-vous déjà relevé des indices ou identifié le contrevenant ?"
            )
            yield from stream_text_words(text_id, text)
            yield sse_event({"type": "text-end", "id": text_id})

        else:
            text = (
                "Bonjour ! Je suis l'assistant réglementaire de Stop Dépôt Sauvage.\n\n"
                "Je peux vous accompagner pour :\n"
                "- Connaître les règles et délais des procédures administratives et pénales.\n"
                "- Vérifier les pouvoirs de police du maire ou des agents assermentés.\n"
                "- **Préparer une constatation** et générer votre brouillon en quelques secondes.\n\n"
                "Décrivez-moi le dépôt constaté ou posez-moi votre question juridique !"
            )
            yield from stream_text_words(text_id, text)
            yield sse_event({"type": "text-end", "id": text_id})


class OpenAICompatibleAIAdapter(BaseAIAdapter):
    """Generic adapter for OpenRouter, Mistral, Albert, or any OpenAI-compatible provider."""

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str,
        timeout: int = 40,
        system_prompt: Optional[str] = None,
        debug_mode: bool = False,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.system_prompt = system_prompt or SYSTEM_PROMPT
        self.debug_mode = debug_mode

    def stream_chat(
        self, messages: List[Dict[str, Any]], context: Optional[Dict[str, Any]] = None
    ) -> Generator[str, None, None]:
        text_id = f"txt_{uuid.uuid4().hex[:8]}"

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        openai_messages = [{"role": "system", "content": self.system_prompt}]

        if context:
            ctx_desc = []
            if profil := context.get("profil_usager"):
                ctx_desc.append(f"Profil usager : {profil} ({context.get('procedures_count', 0)} procédure(s) enregistrée(s))")
            if current_path := context.get("current_path") or context.get("currentPath"):
                ctx_desc.append(f"Page active : {current_path}")
            if dossier_actif := context.get("dossier_actif"):
                ctx_desc.append(f"Dossier consulté à l'écran #{dossier_actif.get('id')} : étape '{dossier_actif.get('etape_metier')}', volume {dossier_actif.get('volume_estime')}, auteur identifié : {dossier_actif.get('auteur_identifie')}, statut AR : {dossier_actif.get('ar_statut')}")
            elif dossiers := context.get("dossiers_recents"):
                recap_dossiers = ", ".join(f"#{d.get('id')} ({d.get('etape_metier')})" for d in dossiers[:3])
                ctx_desc.append(f"Historique passif des dossiers : {recap_dossiers}")

            if ctx_desc:
                openai_messages.append(
                    {
                        "role": "system",
                        "content": "Contexte de session (Information d'arrière-plan passive - NE PAS en parler sauf demande expresse de l'usager) : " + " | ".join(ctx_desc),
                    }
                )

        # Recherche documentaire ciblée sur les 2 derniers messages utilisateur avec concaténation multi-tours
        user_queries = []
        for m in reversed(messages):
            if m.get("role") == "user":
                c = m.get("content", "")
                if not c and isinstance(m.get("parts"), list):
                    c = "".join(p.get("text", "") for p in m.get("parts", []) if isinstance(p, dict) and p.get("type") == "text")
                if isinstance(c, str) and c.strip():
                    user_queries.append(c.strip())
                elif isinstance(c, list):
                    joined = " ".join(p.get("text", "") for p in c if isinstance(p, dict)).strip()
                    if joined:
                        user_queries.append(joined)
                if len(user_queries) >= 2:
                    break

        combined_query = " ".join(reversed(user_queries))
        if combined_query:
            try:
                retriever = get_retriever()
                relevant_docs = retriever.search(combined_query, top_k=2)
                if relevant_docs:
                    rag_context_blocks = []
                    for doc in relevant_docs:
                        rag_context_blocks.append(
                            f"### Source : {doc['source']} ({doc['title']})\n{doc['content']}"
                        )
                    rag_system_message = (
                        "DOCUMENTS OFFICIELS ET JURIDIQUES DE RÉFÉRENCE (À respecter impérativement) :\n\n"
                        + "\n\n---\n\n".join(rag_context_blocks)
                        + "\n\nCONSIGNE : Utilise ces documents officiels pour formuler une réponse juridiquement exacte."
                    )
                    openai_messages.append(
                        {"role": "system", "content": rag_system_message}
                    )
            except Exception as e:
                logger.warning("Error retrieving knowledge docs: %s", e)

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if not content and isinstance(msg.get("parts"), list):
                # Vercel AI SDK v4 format: message content is in parts: [{type: 'text', text: '...'}]
                content = "".join(
                    p.get("text", "")
                    for p in msg.get("parts", [])
                    if isinstance(p, dict) and p.get("type") == "text"
                )
            elif isinstance(content, list):
                text_content = ""
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        text_content += part.get("text", "")
                content = text_content

            content_str = str(content).strip() if content is not None else ""
            if role == "user":
                # Épuration anti-PII stricte avant toute transmission à l'API LLM
                content_str = scrub_pii(content_str)


            # Check if this message contained a tool call or tool result
            tool_calls = msg.get("tool_calls")
            if not tool_calls and isinstance(msg.get("parts"), list):
                # Extract tool calls from Vercel AI SDK parts format if present
                for part in msg.get("parts", []):
                    if isinstance(part, dict) and part.get("type") in ("tool-input-available", "tool-call"):
                        tool_calls = [{
                            "id": part.get("toolCallId") or part.get("id") or f"call_{uuid.uuid4().hex[:8]}",
                            "type": "function",
                            "function": {
                                "name": part.get("toolName") or part.get("name", ""),
                                "arguments": json.dumps(part.get("input") or part.get("args") or {}, ensure_ascii=False),
                            }
                        }]
                        break

            # Albert / vLLM requires:
            # 1. assistant messages must have either non-empty content or non-empty tool_calls
            # 2. empty placeholder assistant messages must be ignored
            if role == "assistant":
                if not content_str and not tool_calls:
                    continue
                msg_entry: Dict[str, Any] = {"role": "assistant"}
                if content_str:
                    msg_entry["content"] = content_str
                else:
                    msg_entry["content"] = ""
                if tool_calls:
                    msg_entry["tool_calls"] = tool_calls
                openai_messages.append(msg_entry)
            elif role == "user":
                if not content_str:
                    continue
                openai_messages.append({"role": "user", "content": content_str})
            else:
                openai_messages.append({"role": role, "content": content_str})

        # Albert rejects requests where the final message is from the assistant
        while openai_messages and openai_messages[-1].get("role") == "assistant":
            openai_messages.pop()

        payload = {
            "model": self.model,
            "messages": openai_messages,
            "tools": [TOOL_PROPOSE_CONSTATATION_DRAFT],
            "tool_choice": "auto",
            "stream": True,
        }

        if self.debug_mode:
            logger.info(
                "\n==================== [CHATBOT AI DEBUG REQUEST] ====================\n"
                "Target URL : %s\n"
                "Model      : %s\n"
                "Timeout    : %ss\n"
                "Messages count : %d\n"
                "--- FULL PROMPTS & MESSAGES ---\n%s\n"
                "--- TOOLS CONFIG ---\n%s\n"
                "====================================================================",
                url,
                self.model,
                self.timeout,
                len(openai_messages),
                json.dumps(openai_messages, indent=2, ensure_ascii=False),
                json.dumps(payload.get("tools"), indent=2, ensure_ascii=False),
            )

        try:
            resp = requests.post(
                url, headers=headers, json=payload, stream=True, timeout=self.timeout
            )
            if not resp.ok:
                logger.error("LLM API returned error %s: %s | Payload sent: %s", resp.status_code, resp.text, json.dumps(payload, ensure_ascii=False))
            resp.raise_for_status()
        except Exception as e:
            logger.exception("Error during LLM request to %s: %s", url, e)
            yield sse_event(
                {
                    "type": "error",
                    "errorText": "Erreur de communication avec le fournisseur d'IA.",
                }
            )
            return

        yield sse_event({"type": "text-start", "id": text_id})

        accumulated_tool_call: Optional[Dict[str, Any]] = None
        accumulated_text_chunks: List[str] = []

        for line in resp.iter_lines():
            if not line:
                continue
            decoded_line = line.decode("utf-8")
            if not decoded_line.startswith("data: "):
                continue
            data_str = decoded_line[6:].strip()
            if data_str == "[DONE]":
                break

            try:
                chunk = json.loads(data_str)
                choices = chunk.get("choices") or []
                if not choices:
                    continue
                choice = choices[0]
                delta = choice.get("delta", {})

                if content_delta := delta.get("content"):
                    # Filtrage préventif des balises vLLM/DeepSeek d'appel d'outil
                    if "</｜DSML｜" in content_delta or "<｜DSML｜" in content_delta:
                        continue
                    if self.debug_mode:
                        accumulated_text_chunks.append(content_delta)
                    yield sse_event(
                        {"type": "text-delta", "id": text_id, "delta": content_delta}
                    )

                if tool_calls := delta.get("tool_calls"):
                    for tc in tool_calls:
                        if accumulated_tool_call is None:
                            accumulated_tool_call = {
                                "id": tc.get("id") or f"call_{uuid.uuid4().hex[:8]}",
                                "name": tc.get("function", {}).get("name", ""),
                                "arguments": tc.get("function", {}).get(
                                    "arguments", ""
                                ),
                            }
                        else:
                            if fn := tc.get("function"):
                                if fn_name := fn.get("name"):
                                    accumulated_tool_call["name"] = fn_name
                                if args_chunk := fn.get("arguments"):
                                    accumulated_tool_call["arguments"] += args_chunk

            except Exception as e:
                logger.warning("Error decoding LLM chunk: %s", e)
                continue

        yield sse_event({"type": "text-end", "id": text_id})

        if self.debug_mode:
            logger.info(
                "\n==================== [CHATBOT AI DEBUG RESPONSE] ====================\n"
                "Model               : %s\n"
                "Streamed text response :\n%s\n"
                "Accumulated tool call  : %s\n"
                "=====================================================================",
                self.model,
                "".join(accumulated_text_chunks),
                json.dumps(accumulated_tool_call, indent=2, ensure_ascii=False) if accumulated_tool_call else "None",
            )

        if accumulated_tool_call and accumulated_tool_call.get("name"):
            try:
                args = json.loads(accumulated_tool_call["arguments"] or "{}")
            except Exception:
                args = {}

            yield sse_event(
                {
                    "type": "tool-input-available",
                    "toolCallId": accumulated_tool_call["id"],
                    "toolName": accumulated_tool_call["name"],
                    "input": args,
                }
            )
        else:
            # Fallback de secours : si le LLM a cité l'outil propose_constatation_draft dans son texte
            # ou s'il s'agit manifestement d'une constatation de dépôt sans appel formel d'outil émis par le provider
            full_response_text = "".join(accumulated_text_chunks)
            if "propose_constatation_draft" in full_response_text:
                # Extraire ou déduire les paramètres du message utilisateur et du texte généré
                last_user_query = ""
                for msg in reversed(messages):
                    if msg.get("role") == "user":
                        c = msg.get("content", "")
                        last_user_query = c if isinstance(c, str) else str(c)
                        break

                types_depot = []
                combined_low = (last_user_query + " " + full_response_text).lower()
                if "gravat" in combined_low:
                    types_depot.append("Gravats")
                if "pneu" in combined_low:
                    types_depot.append("Pneus")
                if "amiante" in combined_low:
                    types_depot.append("Amiante")
                if "vert" in combined_low:
                    types_depot.append("Déchets verts")
                if "véhicule" in combined_low or "vhu" in combined_low or "voiture" in combined_low or "épave" in combined_low:
                    types_depot.append("Véhicule / VHU")
                if not types_depot:
                    types_depot = ["Encombrants"]

                volume = "Entre 1 et 3m3"
                volume_m3 = 2.0
                if "10" in combined_low or "important" in combined_low:
                    volume = "Entre 3 et 10m3"
                    volume_m3 = 6.0
                elif "moins de 1" in combined_low or "petit" in combined_low or "sac" in combined_low:
                    volume = "Moins de 1m3"
                    volume_m3 = 0.5

                fallback_tool_call = {
                    "type": "tool-input-available",
                    "toolCallId": f"call_fallback_{uuid.uuid4().hex[:8]}",
                    "toolName": "propose_constatation_draft",
                    "input": {
                        "commune": "",
                        "localisationDepot": "Voirie / chemin communal",
                        "volumeDepot": volume,
                        "volumeM3": volume_m3,
                        "typesDepot": types_depot,
                        "natureTerrain": ["domaine public"],
                        "auteurIdentifie": False,
                        "precisionsDepot": f"Généré suite au signalement : {last_user_query[:150]}",
                    },
                }
                yield sse_event(fallback_tool_call)


def get_ai_adapter() -> BaseAIAdapter:
    """
    Instantiate the AI adapter.
    Priority: ChatbotConfig (Database Singleton) > Django settings / Environment variables.
    """
    # Récupération de la configuration en base de données
    db_config = None
    try:
        db_config = ChatbotConfig.get_solo()
    except Exception as e:
        logger.warning("Could not load ChatbotConfig from database: %s", e)

    provider = (
        (db_config.provider if db_config and db_config.provider else None)
        or "mock"
    ).lower()

    api_key = (
        (db_config.api_key if db_config and db_config.api_key else None)
        or ""
    )
    model = (
        (db_config.model if db_config and db_config.model else None)
        or ""
    )
    base_url = (
        (db_config.base_url if db_config and db_config.base_url else None)
        or ""
    )
    timeout = (
        (db_config.timeout if db_config and db_config.timeout else None)
        or 40
    )
    system_prompt = (
        (db_config.system_prompt if db_config and db_config.system_prompt else None)
        or SYSTEM_PROMPT
    )
    debug_mode = bool(getattr(settings, "AI_DEBUG", False))

    if provider == "mock":
        return MockAIAdapter(debug_mode=debug_mode)

    if provider in ("openrouter", "openrouter-api"):
        base_url = base_url or "https://openrouter.ai/api/v1"
        model = model or "~deepseek/deepseek-v4-flash-latest"
        return OpenAICompatibleAIAdapter(
            api_key=api_key,
            model=model,
            base_url=base_url,
            timeout=timeout,
            system_prompt=system_prompt,
            debug_mode=debug_mode,
        )

    if provider == "mistral":
        base_url = base_url or "https://api.mistral.ai/v1"
        model = model or "mistral-large-latest"
        return OpenAICompatibleAIAdapter(
            api_key=api_key,
            model=model,
            base_url=base_url,
            timeout=timeout,
            system_prompt=system_prompt,
            debug_mode=debug_mode,
        )

    if provider in ("albert", "albert-api"):
        base_url = base_url or "https://albert.api.etalab.gouv.fr/v1"
        model = model or "mistral-small-3-2-24b-instruct-2506"
        return OpenAICompatibleAIAdapter(
            api_key=api_key,
            model=model,
            base_url=base_url,
            timeout=timeout,
            system_prompt=system_prompt,
            debug_mode=debug_mode,
        )

    if provider == "custom":
        return OpenAICompatibleAIAdapter(
            api_key=api_key,
            model=model,
            base_url=base_url,
            timeout=timeout,
            system_prompt=system_prompt,
            debug_mode=debug_mode,
        )

    logger.warning("Unknown AI provider '%s', falling back to mock.", provider)
    return MockAIAdapter(debug_mode=debug_mode)
