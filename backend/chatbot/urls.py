from django.urls import path
from backend.chatbot.views import (
    BackofficeChatbotConfigView,
    BackofficeChatbotTestConnectionView,
    ChatbotChatView,
)

urlpatterns = [
    path("chat/", ChatbotChatView.as_view(), name="chatbot-chat"),
    path("config/", BackofficeChatbotConfigView.as_view(), name="chatbot-config"),
    path("test-connection/", BackofficeChatbotTestConnectionView.as_view(), name="chatbot-test-connection"),
]
