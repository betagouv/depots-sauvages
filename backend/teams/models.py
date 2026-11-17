from django.conf import settings
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


class UserProfileQuerySet(models.QuerySet):
    def with_team(self):
        """Helper to systematically select_related team on UserProfile queries."""
        return self.select_related("team")


class UserProfile(TimeStampedModel):
    """
    User profile model holding the user's team membership and future preferences/roles.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Utilisateur",
    )
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
        verbose_name="Organisation / Équipe",
    )

    objects = UserProfileQuerySet.as_manager()

    class Meta:
        verbose_name = "profil utilisateur"
        verbose_name_plural = "profils utilisateurs"

    def __str__(self):
        return f"Profil de {self.user} ({self.team.name if self.team else 'Sans équipe'})"


def get_user_team(user):
    """
    Safely retrieves the user's Team instance from UserProfile,
    without raising RelatedObjectDoesNotExist if the profile does not exist yet.
    """
    if not user or not getattr(user, "is_authenticated", False):
        return None
    profile = getattr(user, "profile", None)
    return profile.team if profile else None


def get_user_team_id(user):
    """
    Safely retrieves the user's team_id from UserProfile.
    """
    if not user or not getattr(user, "is_authenticated", False):
        return None
    profile = getattr(user, "profile", None)
    return profile.team_id if profile else None


# Convenience read-only properties on User model to avoid breaking callers
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

_UserModel = get_user_model()


@receiver(post_save, sender=_UserModel)
def _handle_user_post_save_profile(sender, instance, created, **kwargs):
    if hasattr(instance, "_pending_team"):
        profile, _ = UserProfile.objects.get_or_create(user=instance)
        profile.team = instance._pending_team
        profile.save()
        del instance._pending_team


if not hasattr(_UserModel, "team"):

    def _user_team(self):
        profile = getattr(self, "profile", None)
        return profile.team if profile else None

    def _user_team_setter(self, value):
        from backend.teams.models import UserProfile

        if not getattr(self, "pk", None):
            self._pending_team = value
            return
        profile, _ = UserProfile.objects.get_or_create(user=self)
        profile.team = value
        profile.save()

    def _user_team_id(self):
        profile = getattr(self, "profile", None)
        return profile.team_id if profile else None

    _UserModel.team = property(_user_team, _user_team_setter)
    _UserModel.team_id = property(_user_team_id)


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
