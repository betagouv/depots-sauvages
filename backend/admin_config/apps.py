from django.apps import AppConfig


class AdminConfigConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.admin_config"
    verbose_name = "Admin Config"
