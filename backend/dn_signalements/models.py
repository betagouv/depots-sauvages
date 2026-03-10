from django.conf import settings
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


class UserDossier(TimeStampedModel):
    """
    Model for storing a user's dossier summary from Démarche Numérique locally.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dossiers"
    )
    numero_dossier = models.IntegerField("numéro dossier", unique=True)
    date_creation = models.DateTimeField("date de création", null=True, blank=True)
    date_modification = models.DateTimeField("date de modification", null=True, blank=True)
    date_constat = models.DateTimeField("date de constat", null=True, blank=True)
    localisation_depot = models.TextField("localisation", blank=True)

    class Meta:
        verbose_name = "dossier"
        verbose_name_plural = "dossiers"

    @property
    def title(self):
        return f"Dossier #{self.numero_dossier}"

    def __str__(self):
        return f"Dossier #{self.numero_dossier} ({self.user.email})"
