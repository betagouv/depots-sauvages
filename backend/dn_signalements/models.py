from django.db import models
from model_utils.models import TimeStampedModel

from backend.signalements.models import AbstractSignalementBase
from backend.signalements.prejudice import PrejudiceMixin


class DNSignalement(AbstractSignalementBase, PrejudiceMixin, TimeStampedModel):
    """
    Model for signalements imported from Démarche Numérique API
    """

    dn_numero_dossier = models.IntegerField("numéro DN", unique=True)
    dn_date_creation = models.DateTimeField("date de création DN", null=True, blank=True)
    dn_date_modification = models.DateTimeField("date modification DN", null=True, blank=True)

    class Meta:
        verbose_name = "signalement DN"
        verbose_name_plural = "signalements DN"

    def __str__(self):
        return f"Dépôt DN #{self.dn_numero_dossier} à {self.commune} le {self.date_constat}"
