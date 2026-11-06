from django.contrib import admin
from solo.admin import SingletonModelAdmin
from backend.chatbot.models import ChatbotConfig


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
        (
            "Débogage & Observabilité",
            {
                "fields": ("debug_mode",),
            },
        ),
    )
