from django.apps import AppConfig


class SignalementsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.signalements"
    verbose_name = "Signalements"

    def ready(self):
        """
        Connect signals when the app is ready
        """
        import backend.signalements.signals  # noqa
