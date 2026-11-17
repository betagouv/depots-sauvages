from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.teams.models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def handle_user_post_save_profile(sender, instance, created, **kwargs):
    if hasattr(instance, "_pending_team"):
        profile, _ = UserProfile.objects.get_or_create(user=instance)
        profile.team = instance._pending_team
        profile.save()
        del instance._pending_team
