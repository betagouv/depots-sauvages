from django.apps import AppConfig


class AntispamTimerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.antispam_timer"
    verbose_name = "Anti-spam Timer"
