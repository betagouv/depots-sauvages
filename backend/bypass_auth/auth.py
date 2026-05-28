from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class BypassAuthBackend(BaseBackend):
    """
    Custom authentication backend that allows credential-free authentication
    for non-privileged test users in non-production environments.
    """

    def authenticate(self, request, email=None, **kwargs):
        if not getattr(settings, "BYPASS_AUTH_ENABLED"):
            return None
        env_name = getattr(settings, "ENV_NAME", "")
        if "prod" in env_name:
            return None
        if not email:
            return None
        return User.objects.filter(username=email, is_staff=False, is_superuser=False).first()

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
