import logging
from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.chatbot.adapters import get_ai_adapter

logger = logging.getLogger(__name__)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication without strict CSRF enforcement for the public chatbot endpoint,
    while still attaching request.user when authenticated via session.
    """

    def enforce_csrf(self, request):
        return


class ChatbotChatView(APIView):
    """
    Streaming conversation endpoint for the chatbot.
    Publicly accessible (AllowAny) with Server-Sent Events (SSE).
    """

    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        messages = data.get("messages", [])
        context = data.get("context", {})

        if request.user and request.user.is_authenticated:
            context.setdefault(
                "userRole",
                getattr(request.user, "role", "Agent public / Élu"),
            )
            context.setdefault(
                "userCommune",
                getattr(request.user, "commune", ""),
            )

        adapter = get_ai_adapter()

        try:
            stream_gen = adapter.stream_chat(messages=messages, context=context)
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
