from django.apps import AppConfig


class TeamsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.teams"
    verbose_name = "Organisations & Équipes"

    def ready(self):
        import backend.teams.signals  # noqa
