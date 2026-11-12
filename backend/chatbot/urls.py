from django.urls import path
from backend.chatbot.views import (
    BackofficeChatbotConfigView,
    BackofficeChatbotConversationDetailView,
    BackofficeChatbotConversationListView,
    BackofficeChatbotTestConnectionView,
    ChatbotChatView,
    ChatbotFeedbackView,
)

urlpatterns = [
    path("chat/", ChatbotChatView.as_view(), name="chatbot-chat"),
    path("feedback/", ChatbotFeedbackView.as_view(), name="chatbot-feedback"),
    path("config/", BackofficeChatbotConfigView.as_view(), name="chatbot-config"),
    path("test-connection/", BackofficeChatbotTestConnectionView.as_view(), name="chatbot-test-connection"),
    path("conversations/", BackofficeChatbotConversationListView.as_view(), name="chatbot-conversations-list"),
    path("conversations/<uuid:pk>/", BackofficeChatbotConversationDetailView.as_view(), name="chatbot-conversations-detail"),
]
