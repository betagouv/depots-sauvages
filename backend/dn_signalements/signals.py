from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .tasks import sync_user_dossiers


@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    """
    Trigger dossier synchronization when a user logs in.
    """
    sync_user_dossiers.enqueue(user.id)
