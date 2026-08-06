from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from backend.activity_logs.tracking import IdempotentTrackingHandler
from backend.activity_logs.utils import resolve_auth_method
from backend.stats.anonymizer import anonymize_user_hash


@receiver(user_logged_in)
def track_user_logged_in(sender, request, user, **kwargs):
    try:
        IdempotentTrackingHandler().track_action(
            {
                "action": "utilisateur_connecte",
                "actor": anonymize_user_hash(user.id),
                "target": "session",
                "session_id": getattr(request.session, "session_key", None),
                "data": {
                    "user_is_staff": user.is_staff,
                    "auth_method": resolve_auth_method(request),
                },
            },
            model_alias="activity_log",
        )
    except Exception:
        # In test environments without stats_db allowed or when database is unreachable
        pass
