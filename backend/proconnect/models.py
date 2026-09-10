from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class ProConnectProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="proconnect_profile",
        verbose_name="Utilisateur",
    )
    sub = models.CharField(max_length=255, blank=True, db_index=True, verbose_name="Sub ProConnect")
    siret = models.CharField(max_length=14, blank=True, db_index=True, verbose_name="SIRET")
    siren = models.CharField(max_length=9, blank=True, db_index=True, verbose_name="SIREN")
    organization_label = models.CharField(
        max_length=255, blank=True, verbose_name="Nom de l'organisation"
    )
    roles = models.JSONField(default=list, blank=True, verbose_name="Rôles ProConnect")
    raw_claims = models.JSONField(default=dict, blank=True, verbose_name="Claims bruts OIDC")

    class Meta:
        verbose_name = "Profil ProConnect"
        verbose_name_plural = "Profils ProConnect"

    def __str__(self):
        return f"{self.user.email} - {self.organization_label or self.siret or 'Sans organisation'}"
