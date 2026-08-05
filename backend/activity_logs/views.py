from backend.activity_logs.models import ActivityLog
from backend.stats.anonymizer import anonymize_user_hash
from backend.stats.models import StatsSuiviProcedure


class TrackActivityMixin:
    def _track(self, action, target, constatation_id=None, **data):
        suivi_procedure_id = None
        if constatation_id is not None:
            suivi_procedure_id = (
                StatsSuiviProcedure.objects.filter(constatation_id=constatation_id)
                .values_list("id", flat=True)
                .first()
            )
        ActivityLog.objects.create(
            action=action,
            actor=anonymize_user_hash(self.request.user.id),
            target=target,
            constatation_id=constatation_id,
            suivi_procedure_id=suivi_procedure_id,
            data={
                "user_is_staff": self.request.user.is_staff,
                **data,
            },
        )
