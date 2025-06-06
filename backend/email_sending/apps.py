from django.apps import AppConfig


class EmailSendingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.email_sending"
    verbose_name = "Envoie d'emails"
