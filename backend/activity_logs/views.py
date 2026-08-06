from backend.activity_logs.tracking import IdempotentTrackingHandler
from backend.procedures.models import SuiviProcedure
from backend.stats.anonymizer import anonymize_user_hash


class TrackActivityMixin:
    def _track(self, action, target, constatation_id=None, **data):
        suivi_procedure_id = None
        if constatation_id is not None:
            suivi_procedure_id = (
                SuiviProcedure.objects.filter(constatation_id=constatation_id)
                .values_list("id", flat=True)
                .first()
            )
        IdempotentTrackingHandler().track_action(
            {
                "action": action,
                "actor": anonymize_user_hash(self.request.user.id),
                "target": target,
                "constatation_id": constatation_id,
                "suivi_procedure_id": suivi_procedure_id,
                "session_id": getattr(self.request.session, "session_key", None),
                "data": {
                    "user_is_staff": self.request.user.is_staff,
                    **data,
                },
            },
            model_alias="activity_log",
        )
