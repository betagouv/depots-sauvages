import json
import logging
from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.chatbot.adapters import get_ai_adapter
from backend.chatbot.context import build_safe_user_context
from backend.chatbot.models import ChatbotConfig
from backend.chatbot.serializers import ChatbotConfigSerializer

logger = logging.getLogger(__name__)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication without strict CSRF enforcement for the chatbot endpoint,
    while still attaching request.user when authenticated via session.
    """

    def enforce_csrf(self, request):
        return


class ChatbotChatView(APIView):
    """
    Streaming conversation endpoint for the chatbot.
    Reserved for authenticated users (IsAuthenticated) with Server-Sent Events (SSE).
    Builds a strictly anonymized (Zero-PII) context.
    """

    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        messages = data.get("messages", [])
        raw_client_context = data.get("context", {})
        current_path = raw_client_context.get("currentPath", "")

        # Construction du contexte sécurisé et anonymisé Zero-PII
        safe_context = build_safe_user_context(
            user=request.user, current_path=current_path
        )

        adapter = get_ai_adapter()

        try:
            stream_gen = adapter.stream_chat(messages=messages, context=safe_context)
            response = StreamingHttpResponse(
                stream_gen,
                content_type="text/event-stream; charset=utf-8",
            )
            response["Cache-Control"] = "no-cache, no-transform"
            response["X-Accel-Buffering"] = "no"
            return response
        except Exception as e:
            logger.exception("Error executing chatbot stream: %s", e)
            return Response(
                {"error": "An error occurred while communicating with the chatbot."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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

        from urllib.parse import urlparse
        parsed = urlparse(base_url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            return Response(
                {
                    "success": False,
                    "error": "Format d'URL de base invalide (doit commencer par http:// ou https://).",
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
        except Exception as e:
            logger.warning("Error testing LLM API connection: %s", e)
            return Response(
                {
                    "success": False,
                    "error": f"Erreur de communication avec l'API : {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

