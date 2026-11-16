from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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

    def save(self, *args, **kwargs):
        self.siret = (self.siret or "").strip()
        self.siren = (self.siren or "").strip()
        if self.siret and len(self.siret) >= 9 and not self.siren:
            self.siren = self.siret[:9]
        super().save(*args, **kwargs)


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

    def clean(self):
        super().clean()
        self.siret = (self.siret or "").strip()
        self.siren = (self.siren or "").strip()
        if not self.siret and not self.siren:
            raise ValidationError("Au moins un SIREN ou un SIRET doit être renseigné.")
        if self.siret and (len(self.siret) != 14 or not self.siret.isdigit()):
            raise ValidationError({"siret": "Le SIRET doit comporter exactement 14 chiffres."})
        if self.siren and (len(self.siren) != 9 or not self.siren.isdigit()):
            raise ValidationError({"siren": "Le SIREN doit comporter exactement 9 chiffres."})
        if self.siret and self.siren and self.siret[:9] != self.siren:
            raise ValidationError("Le SIREN ne correspond pas aux 9 premiers chiffres du SIRET.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @classmethod
    def is_excluded(cls, siret: str = "", siren: str = "") -> bool:
        """
        Check if a SIRET or SIREN is excluded from automatic team creation.
        """
        siret = (siret or "").strip()
        siren = (siren or "").strip()
        if not siren and len(siret) >= 9:
            siren = siret[:9]

        if not siret and not siren:
            return False

        q = models.Q()
        if siret:
            q |= models.Q(siret=siret)
        if siren:
            q |= models.Q(siren=siren)

        return cls.objects.filter(q).exists()
