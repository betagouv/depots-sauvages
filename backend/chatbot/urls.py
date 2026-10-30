from django.urls import path
from backend.chatbot.views import ChatbotChatView

urlpatterns = [
    path("chat/", ChatbotChatView.as_view(), name="chatbot-chat"),
]
