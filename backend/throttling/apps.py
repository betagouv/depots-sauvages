from django.apps import AppConfig


class ThrottlingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.throttling"
    verbose_name = "Throttling"
