import json
import logging
import uuid
from pathlib import Path

from django.conf import settings
from django.db import models
from solo.models import SingletonModel

logger = logging.getLogger(__name__)

FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "chatbot_config.json"


def get_default_system_prompt():
    try:
        if FIXTURE_PATH.exists():
            data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
            if data and isinstance(data, list):
                return data[0].get("fields", {}).get("system_prompt", "")
    except Exception as e:
        logger.warning("Could not read default system prompt from fixture: %s", e)
    return ""


class ChatbotConfig(SingletonModel):
    PROVIDER_CHOICES = [
        ("mock", "Mock (Simulateur local sans coût)"),
        ("openrouter", "OpenRouter"),
        ("mistral", "Mistral AI"),
        ("albert", "Albert (Étalab / DINUM)"),
        ("custom", "OpenAI-compatible personnalisé"),
    ]

    provider = models.CharField(
        max_length=50,
        choices=PROVIDER_CHOICES,
        default="mock",
        verbose_name="Fournisseur d'IA",
        help_text="Fournisseur d'IA utilisé pour générer les réponses.",
    )
    model = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Modèle LLM",
        help_text="Nom/identifiant du modèle (ex: deepseek/deepseek-v4-flash-latest, mistral-large-latest).",
    )
    api_key = models.CharField(
        max_length=500,
        blank=True,
        default="",
        verbose_name="Clé d'API",
        help_text="Clé d'accès API du fournisseur.",
    )
    base_url = models.CharField(
        max_length=500,
        blank=True,
        default="",
        verbose_name="URL de base de l'API",
        help_text="URL personnalisée (si vide, l'URL officielle du provider sera utilisée).",
    )
    timeout = models.PositiveIntegerField(
        default=40,
        verbose_name="Timeout (secondes)",
        help_text="Délai maximum d'attente d'une réponse de l'API LLM.",
    )
    system_prompt = models.TextField(
        default="",
        blank=True,
        verbose_name="Prompt système",
        help_text="Instructions maîtresses guidant les réponses, le ton et les garde-fous du chatbot.",
    )

    class Meta:
        verbose_name = "Configuration du Chatbot"
        verbose_name_plural = "Configuration du Chatbot"

    def __str__(self):
        return f"Configuration Chatbot ({self.provider} - {self.model or 'défaut'})"


class ChatbotConversation(models.Model):
    FEEDBACK_CHOICES = [
        ("", "Aucun"),
        ("up", "Utile"),
        ("down", "À améliorer"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Identifiant de conversation",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="chatbot_conversations",
        verbose_name="Utilisateur",
    )
    current_path = models.CharField(
        max_length=500,
        blank=True,
        default="",
        verbose_name="Page d'origine",
    )
    messages = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Messages (expurgés Zero-PII)",
        help_text="Historique des échanges de la conversation (questions usager filtrées et réponses assistant).",
    )
    has_draft_proposed = models.BooleanField(
        default=False,
        verbose_name="Brouillon proposé",
    )
    feedback = models.CharField(
        max_length=20,
        blank=True,
        default="",
        choices=FEEDBACK_CHOICES,
        verbose_name="Appréciation usager",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de début",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernier échange",
    )

    class Meta:
        verbose_name = "Conversation Chatbot"
        verbose_name_plural = "Conversations Chatbot"
        ordering = ["-updated_at"]

    def __str__(self):
        user_label = (
            self.user.email if self.user and getattr(self.user, "email", None) else "Utilisateur"
        )
        return f"Conversation {str(self.id)[:8]} ({user_label})"
