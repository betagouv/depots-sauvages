from django.apps import AppConfig


class ConstatationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.constatations"
    verbose_name = "Constatations"

    def ready(self):
        import backend.constatations.signals  # noqa
