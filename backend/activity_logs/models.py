from django.db import models
from trackman.models import TrackingActionModel


class ActivityLog(TrackingActionModel):
    constatation = models.ForeignKey(
        "stats.StatsConstatation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_constraint=False,
        related_name="activity_logs",
        verbose_name="Constatation liée",
    )
    suivi_procedure = models.ForeignKey(
        "stats.StatsSuiviProcedure",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_constraint=False,
        related_name="activity_logs",
        verbose_name="Suivi de procédure lié",
    )

    class Meta:
        db_table = "stats_activity_log"
        verbose_name = "Log d'activité"
        verbose_name_plural = "Logs d'activités"
