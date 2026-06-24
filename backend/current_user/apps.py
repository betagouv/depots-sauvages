from django.apps import AppConfig


class CurrentUserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.current_user"
    verbose_name = "Current User"
