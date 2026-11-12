from django.contrib import admin
from solo.admin import SingletonModelAdmin

from backend.chatbot.models import ChatbotConfig, ChatbotConversation


@admin.register(ChatbotConfig)
class ChatbotConfigAdmin(SingletonModelAdmin):
    fieldsets = (
        (
            "Moteur & Modèle IA",
            {
                "fields": (
                    "provider",
                    "model",
                    "api_key",
                    "base_url",
                    "timeout",
                )
            },
        ),
        (
            "Instructions Système (Prompt)",
            {
                "fields": ("system_prompt",),
            },
        ),
    )


@admin.register(ChatbotConversation)
class ChatbotConversationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "current_path",
        "has_draft_proposed",
        "feedback",
        "created_at",
        "updated_at",
    )
    list_filter = ("has_draft_proposed", "feedback", "created_at")
    search_fields = ("user__email", "user__first_name", "user__last_name", "current_path")
    readonly_fields = ("id", "created_at", "updated_at")
