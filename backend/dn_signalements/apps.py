from django.apps import AppConfig


class DnSignalementsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.dn_signalements"
    verbose_name = "DN Signalements"

    def ready(self):
        from django.contrib.auth.signals import user_logged_in
        from django.dispatch import receiver

        @receiver(user_logged_in)
        def trigger_dossier_sync(sender, request, user, **kwargs):
            from .tasks import sync_user_dossiers

            sync_user_dossiers.enqueue(user.id)
