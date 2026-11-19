from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from backend.activity_logs.tracking import IdempotentTrackingHandler
from backend.activity_logs.utils import resolve_auth_method
from backend.stats.anonymizer import anonymize_user_hash
from backend.teams.models import get_user_team_id


@receiver(user_logged_in)
def track_user_logged_in(sender, request, user, **kwargs):
    try:
        log_data = {
            "est_staff": user.is_staff,
            "methode_auth": resolve_auth_method(request),
        }
        team_id = get_user_team_id(user)
        if team_id is not None:
            log_data["team_id"] = team_id
        IdempotentTrackingHandler().track_action(
            {
                "action": "utilisateur_connecte",
                "actor": anonymize_user_hash(user.id),
                "target": "auth",
                "session_id": getattr(request.session, "session_key", None),
                "data": log_data,
            },
            model_alias="activity_log",
        )
    except Exception:
        # In test environments without stats_db allowed or when database is unreachable
        pass
