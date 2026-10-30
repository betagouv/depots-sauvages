import json
import logging
import re
import time
import uuid
from typing import Any, Dict, Generator, List, Optional
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Tu es l'Assistant IA de la plateforme Stop Dépôt Sauvage (Protect'Envi).
Ton rôle est d'accompagner les maires, élus locaux, gardes champêtres, policiers municipaux et agents assermentés dans la gestion et la verbalisation des dépôts sauvages.

Tu apportes des conseils précis basés sur la réglementation en vigueur (Code de l'environnement, Code général des collectivités territoriales, Code pénal) :
- Procédure de police administrative (mise en demeure, astreinte journalière jusqu'à 1500€, consignation, amende administrative jusqu'à 15 000€ selon l'article L. 541-3).
- Procédure pénale (constat d'infraction, procès-verbal transmis au Procureur de la République sous 5 jours, amendes forfaitaires ou contraventions de 5ème classe).
- Guide méthodologique pour la constatation de flagrant délit, relevé des indices et éléments d'identification de l'auteur.

Capacité d'action :
Lorsque l'utilisateur te décrit une situation de dépôt ou exprime le souhait de faire une constatation ou d'engager une procédure, aide-le à récapituler les informations essentielles (commune, type de déchets, volume estimé, type de terrain, auteur éventuel).
Dès que ces informations clés sont rassemblées ou qu'il te demande de préparer la démarche, utilise impérativement l'outil `propose_constatation_draft` pour lui permettre de créer son brouillon en un clic.

Reste concis, structuré, bienveillant et professionnel. Adopte un ton clair conforme aux standards des services publics français."""

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
            if "10" in query or "important" in query or "gros" in query:
                volume = "Entre 3 et 10m3"
            elif "petit" in query or "sac" in query or "moins" in query:
                volume = "Moins de 1m3"

            commune_match = re.search(r"(?:à|a|sur|commune de)\s+([A-ZÀ-Ÿ][a-zà-ÿ\-]+)", last_user_message)
            commune = commune_match.group(1) if commune_match else ""

            tool_call_id = f"call_{uuid.uuid4().hex[:10]}"
            tool_input = {
                "commune": commune,
                "localisationDepot": "Chemin rural / abords de voirie",
                "volumeDepot": volume,
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
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def stream_chat(
        self, messages: List[Dict[str, Any]], context: Optional[Dict[str, Any]] = None
    ) -> Generator[str, None, None]:
        text_id = f"txt_{uuid.uuid4().hex[:8]}"

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        openai_messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        if context:
            ctx_desc = []
            if current_path := context.get("currentPath"):
                ctx_desc.append(f"Page actuelle de l'utilisateur : {current_path}")
            if user_role := context.get("userRole"):
                ctx_desc.append(f"Rôle de l'utilisateur : {user_role}")
            if ctx_desc:
                openai_messages.append(
                    {
                        "role": "system",
                        "content": "Contexte de session : " + " | ".join(ctx_desc),
                    }
                )

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if isinstance(content, list):
                text_content = ""
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        text_content += part.get("text", "")
                content = text_content
            openai_messages.append({"role": role, "content": str(content)})

        payload = {
            "model": self.model,
            "messages": openai_messages,
            "tools": [TOOL_PROPOSE_CONSTATATION_DRAFT],
            "tool_choice": "auto",
            "stream": True,
        }

        try:
            resp = requests.post(
                url, headers=headers, json=payload, stream=True, timeout=self.timeout
            )
            resp.raise_for_status()
        except Exception as e:
            logger.exception("Error during LLM request to %s: %s", url, e)
            yield sse_event(
                {
                    "type": "error",
                    "errorText": f"Erreur de communication avec le fournisseur d'IA : {str(e)}",
                }
            )
            return

        yield sse_event({"type": "text-start", "id": text_id})

        accumulated_tool_call: Optional[Dict[str, Any]] = None

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
                choice = chunk.get("choices", [{}])[0]
                delta = choice.get("delta", {})

                if content_delta := delta.get("content"):
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


def get_ai_adapter() -> BaseAIAdapter:
    """Instantiate the AI adapter configured in settings/environment variables."""
    provider = getattr(settings, "AI_PROVIDER", "mock").lower()

    if provider == "mock":
        return MockAIAdapter()

    api_key = getattr(settings, "AI_API_KEY", "")
    model = getattr(settings, "AI_MODEL", "")
    base_url = getattr(settings, "AI_BASE_URL", "")

    if provider == "openrouter":
        base_url = base_url or "https://openrouter.ai/api/v1"
        model = model or "mistralai/mistral-large-2411"
        return OpenAICompatibleAIAdapter(
            api_key=api_key, model=model, base_url=base_url
        )

    if provider == "mistral":
        base_url = base_url or "https://api.mistral.ai/v1"
        model = model or "mistral-large-latest"
        return OpenAICompatibleAIAdapter(
            api_key=api_key, model=model, base_url=base_url
        )

    if provider == "albert":
        base_url = base_url or "https://albert.api.etalab.gouv.fr/v1"
        model = model or "albert/albert-small"
        return OpenAICompatibleAIAdapter(
            api_key=api_key, model=model, base_url=base_url
        )

    logger.warning("Unknown AI provider '%s', falling back to mock.", provider)
    return MockAIAdapter()
