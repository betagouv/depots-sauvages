from django.db import models
from model_utils.models import TimeStampedModel

from backend.signalements.base import AbstractSignalementBase
from backend.signalements.prejudice import PrejudiceMixin


class DSSignalement(AbstractSignalementBase, PrejudiceMixin, TimeStampedModel):
    """
    Model for signalements imported from Démarches Simplifiées API
    """

    ds_numero_dossier = models.IntegerField("numéro DS", unique=True)
    ds_date_depot = models.DateTimeField("date de dépôt DS", null=True, blank=True)
    ds_date_modification = models.DateTimeField("date modification DS", null=True, blank=True)

    class Meta:
        verbose_name = "signalement DS"
        verbose_name_plural = "signalements DS"

    def __str__(self):
        return f"Dépôt DS #{self.ds_numero_dossier} à {self.commune} le {self.date_constat}"
