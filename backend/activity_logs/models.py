from trackman.models import TrackingActionModel


class ActivityLog(TrackingActionModel):
    class Meta:
        db_table = "stats_activity_log"
        verbose_name = "Log d'activité"
        verbose_name_plural = "Logs d'activités"
