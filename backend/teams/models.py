from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from model_utils.models import TimeStampedModel


class Team(TimeStampedModel):
    name = models.CharField("Nom de l'organisation", max_length=255)
    siret = models.CharField("SIRET", max_length=14, unique=True, db_index=True)
    siren = models.CharField("SIREN", max_length=9, blank=True, db_index=True)
    logo = models.ImageField("Logo", upload_to="team_logos/", blank=True, null=True)

    class Meta:
        verbose_name = "organisation"
        verbose_name_plural = "organisations"

    def __str__(self):
        return f"{self.name} ({self.siret})"


# Dynamically attach 'team' ForeignKey to the User model
_user_model = get_user_model()
if not hasattr(_user_model, "team"):
    models.ForeignKey(
        "teams.Team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
        verbose_name="Organisation / Équipe",
    ).contribute_to_class(_user_model, "team")


class TeamAutoCreationExclusion(TimeStampedModel):
    """
    SIREN or SIRET numbers excluded from automatic Team creation and pooling
    during ProConnect authentication (e.g. national police, ministries, headquarters).
    Users with these identifiers remain in individual mode (user.team is None).
    """

    siren = models.CharField("SIREN", max_length=9, blank=True, db_index=True)
    siret = models.CharField("SIRET", max_length=14, blank=True, db_index=True)
    label = models.CharField("Nom de l'organisme / Direction", max_length=255)
    reason = models.TextField("Motif de l'exclusion", blank=True)

    class Meta:
        verbose_name = "exclusion d'auto-création d'équipe"
        verbose_name_plural = "exclusions d'auto-création d'équipe"

    def __str__(self):
        return f"{self.label} ({self.siret or self.siren})"
