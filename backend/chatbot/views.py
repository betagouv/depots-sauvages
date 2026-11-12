import ipaddress
import json
import logging
import socket
import uuid
from urllib.parse import urlparse
from django.db.models import Q
from django.http import StreamingHttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.chatbot.adapters import get_ai_adapter
from backend.chatbot.context import build_safe_user_context, scrub_pii
from backend.chatbot.models import ChatbotConfig, ChatbotConversation
from backend.chatbot.serializers import (
    ChatbotConfigSerializer,
    ChatbotConversationDetailSerializer,
    ChatbotConversationListSerializer,
)
from backend.throttling.throttles import ChatbotRateThrottle

logger = logging.getLogger(__name__)


def is_safe_external_url(url, allow_private=False):
    """
    Vérifie qu'une URL est sécurisée et ne cible pas le réseau local ou les IP privées (SSRF).
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            return False

        hostname = parsed.hostname
        if not hostname:
            return False

        if allow_private:
            return True

        # Validation de l'adresse IP directe
        try:
            ip = ipaddress.ip_address(hostname)
            return not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast)
        except ValueError:
            pass

        # Résolution DNS pour bloquer les domaines pointant vers localhost / IPs privées
        addr_info = socket.getaddrinfo(hostname, None)
        for item in addr_info:
            resolved_ip = ipaddress.ip_address(item[4][0])
            if resolved_ip.is_private or resolved_ip.is_loopback or resolved_ip.is_link_local or resolved_ip.is_reserved or resolved_ip.is_multicast:
                return False

        return True
    except Exception:
        return False


def _extract_raw_message_text(msg):
    content = msg.get("content", "")
    if isinstance(content, str) and content:
        return content
    if isinstance(parts := msg.get("parts"), list):
        return "".join(
            p.get("text", "")
            for p in parts
            if isinstance(p, dict) and p.get("type") == "text"
        )
    if isinstance(content, list):
        return "".join(
            p.get("text", "")
            for p in content
            if isinstance(p, dict) and p.get("type") == "text"
        )
    return str(content or "")


def _sanitize_client_messages_for_storage(raw_messages, existing_messages):
    """
    Transforme et nettoie les messages transmis par le client en appliquant scrub_pii
    sur chaque message utilisateur, tout en préservant les horodatages et feedbacks existants.
    """
    existing_by_index = {
        idx: m for idx, m in enumerate(existing_messages) if isinstance(m, dict)
    }
    now_iso = timezone.now().isoformat()
    sanitized = []

    for idx, msg in enumerate(raw_messages):
        if not isinstance(msg, dict):
            continue
        role = msg.get("role", "user")
        if role not in ("user", "assistant"):
            continue

        raw_text = _extract_raw_message_text(msg).strip()
        clean_text = scrub_pii(raw_text) if role == "user" else raw_text

        prev = existing_by_index.get(idx, {})
        tool_calls = prev.get("tool_calls", [])
        if not tool_calls and isinstance(msg.get("parts"), list):
            for part in msg.get("parts", []):
                if isinstance(part, dict) and part.get("type") in ("tool-input-available", "tool-call"):
                    tool_calls.append(
                        {
                            "toolCallId": part.get("toolCallId") or part.get("id") or "",
                            "toolName": part.get("toolName") or part.get("name") or "",
                            "input": part.get("input") or part.get("args") or {},
                        }
                    )

        if not clean_text and not tool_calls:
            continue

        entry = {
            "id": msg.get("id") or prev.get("id") or f"msg_{idx}",
            "role": role,
            "content": clean_text,
            "timestamp": prev.get("timestamp") or now_iso,
        }
        if tool_calls:
            entry["tool_calls"] = tool_calls
        if prev.get("feedback"):
            entry["feedback"] = prev["feedback"]

        sanitized.append(entry)

    return sanitized


class ChatbotChatView(APIView):
    """
    Streaming conversation endpoint for the chatbot.
    Reserved for authenticated users (IsAuthenticated) with Server-Sent Events (SSE).
    Builds a strictly anonymized (Zero-PII) context and persists sanitized conversations.
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [ChatbotRateThrottle]

    def _resolve_conversation(self, user, raw_conv_id, current_path=""):
        conv_uuid = None
        if raw_conv_id:
            try:
                conv_uuid = uuid.UUID(str(raw_conv_id))
            except (ValueError, TypeError):
                conv_uuid = None

        if conv_uuid:
            existing = ChatbotConversation.objects.filter(id=conv_uuid, user=user).first()
            if existing:
                if current_path and not existing.current_path:
                    existing.current_path = current_path[:500]
                return existing
            # Si l'UUID n'existe pas encore du tout en base, on le crée avec cet UUID
            if not ChatbotConversation.objects.filter(id=conv_uuid).exists():
                return ChatbotConversation.objects.create(
                    id=conv_uuid,
                    user=user,
                    current_path=(current_path or "")[:500],
                )

        return ChatbotConversation.objects.create(
            user=user,
            current_path=(current_path or "")[:500],
        )

    def post(self, request, *args, **kwargs):
        data = request.data
        messages = data.get("messages", [])
        raw_client_context = data.get("context", {}) if isinstance(data.get("context"), dict) else {}
        current_path = raw_client_context.get("currentPath", "")
        form_context = raw_client_context.get("formContext")
        raw_conv_id = (
            raw_client_context.get("conversationId")
            or data.get("conversationId")
            or data.get("id")
        )

        # Résolution et sauvegarde initiale des messages usager expurgés Zero-PII
        conversation = None
        try:
            conversation = self._resolve_conversation(request.user, raw_conv_id, current_path)
            conversation.messages = _sanitize_client_messages_for_storage(
                messages, conversation.messages or []
            )
            conversation.save(update_fields=["messages", "current_path", "updated_at"])
        except Exception as e:
            logger.warning("Could not initialize ChatbotConversation: %s", e)

        # Construction du contexte sécurisé et anonymisé Zero-PII
        safe_context = build_safe_user_context(
            user=request.user, current_path=current_path, form_context=form_context
        )

        adapter = get_ai_adapter()

        try:
            raw_stream_gen = adapter.stream_chat(messages=messages, context=safe_context)

            def _persisting_stream_wrapper():
                assistant_msg_id = f"txt_{uuid.uuid4().hex[:8]}"
                assistant_text_chunks = []
                assistant_tool_calls = []

                try:
                    for chunk_str in raw_stream_gen:
                        if isinstance(chunk_str, str) and chunk_str.startswith("data: "):
                            try:
                                payload_obj = json.loads(chunk_str[6:].strip())
                                ev_type = payload_obj.get("type")
                                if ev_type == "text-start" and payload_obj.get("id"):
                                    assistant_msg_id = payload_obj["id"]
                                elif ev_type == "text-delta":
                                    assistant_text_chunks.append(payload_obj.get("delta", ""))
                                elif ev_type == "tool-input-available":
                                    assistant_tool_calls.append(
                                        {
                                            "toolCallId": payload_obj.get("toolCallId", ""),
                                            "toolName": payload_obj.get("toolName", ""),
                                            "input": payload_obj.get("input", {}),
                                        }
                                    )
                            except Exception:
                                pass
                        yield chunk_str
                finally:
                    if conversation and (assistant_text_chunks or assistant_tool_calls):
                        try:
                            full_reply = "".join(assistant_text_chunks).strip()
                            assistant_entry = {
                                "id": assistant_msg_id,
                                "role": "assistant",
                                "content": full_reply,
                                "timestamp": timezone.now().isoformat(),
                            }
                            if assistant_tool_calls:
                                assistant_entry["tool_calls"] = assistant_tool_calls

                            updated_msgs = list(conversation.messages or [])
                            updated_msgs.append(assistant_entry)
                            conversation.messages = updated_msgs
                            if any(
                                tc.get("toolName") == "propose_constatation_draft"
                                for tc in assistant_tool_calls
                            ):
                                conversation.has_draft_proposed = True
                            conversation.save(
                                update_fields=["messages", "has_draft_proposed", "updated_at"]
                            )
                        except Exception as save_err:
                            logger.warning("Failed to persist assistant reply: %s", save_err)

            response = StreamingHttpResponse(
                _persisting_stream_wrapper(),
                content_type="text/event-stream; charset=utf-8",
            )
            response["Cache-Control"] = "no-cache, no-transform"
            response["X-Accel-Buffering"] = "no"
            if conversation:
                response["X-Conversation-Id"] = str(conversation.id)
            return response
        except Exception as e:
            logger.exception("Error executing chatbot stream: %s", e)
            return Response(
                {"error": "An error occurred while communicating with the chatbot."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ChatbotFeedbackView(APIView):
    """
    Permet à l'utilisateur connecté d'enregistrer une appréciation (up / down)
    sur un message de l'assistant dans sa conversation active.
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data or {}
        raw_conv_id = data.get("conversationId")
        message_id = data.get("messageId")
        message_index = data.get("messageIndex")
        feedback_val = data.get("feedback", "")

        if feedback_val not in ("up", "down", ""):
            return Response(
                {"error": "Valeur de feedback invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conv = None
        if raw_conv_id:
            try:
                conv_uuid = uuid.UUID(str(raw_conv_id))
                conv = ChatbotConversation.objects.filter(
                    id=conv_uuid, user=request.user
                ).first()
            except (ValueError, TypeError):
                pass

        if not conv:
            conv = (
                ChatbotConversation.objects.filter(user=request.user)
                .order_by("-updated_at")
                .first()
            )

        if not conv:
            return Response(
                {"error": "Conversation introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )

        msgs = list(conv.messages or [])
        target_updated = False

        if message_id:
            for m in msgs:
                if isinstance(m, dict) and m.get("id") == message_id:
                    if feedback_val:
                        m["feedback"] = feedback_val
                    else:
                        m.pop("feedback", None)
                    target_updated = True
                    break

        if not target_updated and isinstance(message_index, int) and 0 <= message_index < len(msgs):
            if isinstance(msgs[message_index], dict):
                if feedback_val:
                    msgs[message_index]["feedback"] = feedback_val
                else:
                    msgs[message_index].pop("feedback", None)
                target_updated = True

        if not target_updated and msgs:
            # Par défaut, appliquer sur le dernier message assistant
            for m in reversed(msgs):
                if isinstance(m, dict) and m.get("role") == "assistant":
                    if feedback_val:
                        m["feedback"] = feedback_val
                    else:
                        m.pop("feedback", None)
                    break

        # Synthèse globale sur la conversation : si au moins un 'down' -> 'down', sinon si 'up' -> 'up'
        all_feedbacks = [
            m.get("feedback") for m in msgs if isinstance(m, dict) and m.get("feedback")
        ]
        if "down" in all_feedbacks:
            conv.feedback = "down"
        elif "up" in all_feedbacks:
            conv.feedback = "up"
        else:
            conv.feedback = ""

        conv.messages = msgs
        conv.save(update_fields=["messages", "feedback", "updated_at"])

        return Response(
            {"success": True, "conversationId": str(conv.id), "feedback": conv.feedback},
            status=status.HTTP_200_OK,
        )


class BackofficeChatbotConfigView(APIView):
    """
    API endpoint for viewing and updating the Chatbot configuration in the backoffice.
    Restricted to staff users (IsAdminUser).
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        config = ChatbotConfig.get_solo()
        serializer = ChatbotConfigSerializer(config)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        config = ChatbotConfig.get_solo()
        data = request.data.copy() if hasattr(request.data, "copy") else dict(request.data)
        # Si api_key n'est pas fournie ou vide lors d'une mise à jour partielle sans volonté de l'effacer :
        # Si le front envoie api_key null ou ne l'envoie pas, on conserve l'existante.
        if "api_key" in data and (data["api_key"] is None or data["api_key"] == ""):
            if data.get("clear_api_key"):
                data["api_key"] = ""
            else:
                data.pop("api_key", None)

        serializer = ChatbotConfigSerializer(config, data=data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        logger.info(
            "Chatbot configuration updated by user %s (%s). Provider: %s, Model: %s",
            request.user.pk,
            request.user.username,
            config.provider,
            config.model,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class BackofficeChatbotTestConnectionView(APIView):
    """
    API endpoint to test LLM provider connectivity and credentials.
    Can test with either existing config or temporary parameters passed in the request body.
    """

    permission_classes = [IsAdminUser]

    def post(self, request):
        import time
        import requests
        from django.conf import settings

        config = ChatbotConfig.get_solo()
        data = request.data or {}

        provider = (data.get("provider") or config.provider or "mock").lower()

        if provider == "mock":
            return Response(
                {
                    "success": True,
                    "message": "Le fournisseur Mock est actif. Aucune connexion externe requise.",
                    "provider": "mock",
                    "latency_ms": 1,
                },
                status=status.HTTP_200_OK,
            )

        # Résolution de la clé d'API : saisie en cours > en base
        api_key = (
            data.get("api_key")
            or config.api_key
            or ""
        )

        if not api_key:
            return Response(
                {
                    "success": False,
                    "error": "Aucune clé d'API fournie ou configurée pour tester la connexion.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Base URL
        base_url = (data.get("base_url") or config.base_url or "").strip()
        if not base_url:
            if provider in ("openrouter", "openrouter-api"):
                base_url = "https://openrouter.ai/api/v1"
            elif provider == "mistral":
                base_url = "https://api.mistral.ai/v1"
            elif provider in ("albert", "albert-api"):
                base_url = "https://albert.api.etalab.gouv.fr/v1"
            else:
                return Response(
                    {
                        "success": False,
                        "error": "URL de base (base_url) requise pour ce fournisseur.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        allow_private_network = bool(getattr(settings, "DEBUG", False))
        if not is_safe_external_url(base_url, allow_private=allow_private_network):
            return Response(
                {
                    "success": False,
                    "error": "URL de base invalide ou non autorisée (les adresses locales et privées sont interdites pour des raisons de sécurité).",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Modèle
        model = data.get("model") or config.model or ""
        if not model:
            if provider in ("openrouter", "openrouter-api"):
                model = "deepseek/deepseek-v4-flash-latest"
            elif provider == "mistral":
                model = "mistral-large-latest"
            elif provider in ("albert", "albert-api"):
                model = "mistral-small-3-2-24b-instruct-2506"
            else:
                model = "gpt-3.5-turbo"

        url = f"{base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        test_payload = {
            "model": model,
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 5,
        }

        timeout = int(data.get("timeout") or config.timeout or 15)
        start_time = time.time()

        debug_mode = bool(getattr(settings, "AI_DEBUG", False))
        if debug_mode:
            logger.info(
                "\n==================== [CHATBOT TEST CONNECTION DEBUG REQUEST] ====================\n"
                "Target URL : %s\n"
                "Provider   : %s\n"
                "Model      : %s\n"
                "Timeout    : %ss\n"
                "Payload    : %s\n"
                "==================================================================================",
                url,
                provider,
                model,
                min(timeout, 20),
                json.dumps(test_payload, indent=2, ensure_ascii=False),
            )

        try:
            resp = requests.post(url, headers=headers, json=test_payload, timeout=min(timeout, 20))
            latency_ms = int((time.time() - start_time) * 1000)

            if debug_mode:
                logger.info(
                    "\n==================== [CHATBOT TEST CONNECTION DEBUG RESPONSE] ====================\n"
                    "Status Code : %s\n"
                    "Latency     : %sms\n"
                    "Raw Body    : %s\n"
                    "==================================================================================",
                    getattr(resp, "status_code", None),
                    latency_ms,
                    getattr(resp, "text", ""),
                )

            if resp.status_code == 200:
                result_json = resp.json()
                sample_reply = ""
                try:
                    sample_reply = result_json["choices"][0]["message"]["content"].strip()
                except Exception:
                    pass

                return Response(
                    {
                        "success": True,
                        "message": f"Connexion réussie avec succès au modèle '{model}' ({latency_ms} ms).",
                        "provider": provider,
                        "model": model,
                        "latency_ms": latency_ms,
                        "sample_reply": sample_reply,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                err_text = resp.text[:300]
                return Response(
                    {
                        "success": False,
                        "error": f"L'API a répondu avec le statut HTTP {resp.status_code} : {err_text}",
                        "status_code": resp.status_code,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except requests.exceptions.Timeout:
            return Response(
                {
                    "success": False,
                    "error": f"Délai d'attente dépassé lors de la tentative de connexion à {url}.",
                },
                status=status.HTTP_504_GATEWAY_TIMEOUT,
            )
        except Exception:
            logger.exception("Error testing LLM API connection")
            return Response(
                {
                    "success": False,
                    "error": "Erreur interne lors du test de connexion à l'API.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BackofficeChatbotConversationListView(APIView):
    """
    Liste paginée et filtrable des conversations du chatbot pour le suivi backoffice.
    Accessible aux membres de l'équipe (IsAdminUser).
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        from django.db.models import TextField
        from django.db.models.functions import Cast

        qs = ChatbotConversation.objects.select_related("user").all()

        # Statistiques globales rapides
        total_conversations = qs.count()
        drafts_count = qs.filter(has_draft_proposed=True).count()
        positive_count = qs.filter(feedback="up").count()
        negative_count = qs.filter(feedback="down").count()

        search = (request.query_params.get("search") or "").strip()
        if search:
            qs = qs.annotate(messages_text=Cast("messages", output_field=TextField())).filter(
                Q(user__email__icontains=search)
                | Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
                | Q(current_path__icontains=search)
                | Q(messages_text__icontains=search)
            )

        has_draft = (request.query_params.get("has_draft") or "").strip().lower()
        if has_draft == "true":
            qs = qs.filter(has_draft_proposed=True)
        elif has_draft == "false":
            qs = qs.filter(has_draft_proposed=False)

        feedback_filter = (request.query_params.get("feedback") or "").strip().lower()
        if feedback_filter in ("up", "down"):
            qs = qs.filter(feedback=feedback_filter)
        elif feedback_filter == "none":
            qs = qs.filter(feedback="")

        filtered_count = qs.count()

        try:
            page = max(1, int(request.query_params.get("page", 1)))
        except (ValueError, TypeError):
            page = 1

        try:
            page_size = min(100, max(1, int(request.query_params.get("page_size", 20))))
        except (ValueError, TypeError):
            page_size = 20

        offset = (page - 1) * page_size
        items = qs[offset : offset + page_size]

        serializer = ChatbotConversationListSerializer(items, many=True)
        return Response(
            {
                "count": filtered_count,
                "page": page,
                "page_size": page_size,
                "stats": {
                    "total_conversations": total_conversations,
                    "drafts_count": drafts_count,
                    "positive_count": positive_count,
                    "negative_count": negative_count,
                },
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class BackofficeChatbotConversationDetailView(APIView):
    """
    Consultation détaillée ou suppression d'une conversation du chatbot dans le backoffice.
    """

    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        conv = (
            ChatbotConversation.objects.select_related("user")
            .filter(pk=pk)
            .first()
        )
        if not conv:
            return Response(
                {"error": "Conversation introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ChatbotConversationDetailSerializer(conv)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        conv = ChatbotConversation.objects.filter(pk=pk).first()
        if not conv:
            return Response(
                {"error": "Conversation introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )
        conv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


