import logging
from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.chatbot.adapters import get_ai_adapter
from backend.chatbot.context import build_safe_user_context

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

