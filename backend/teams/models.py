from django.conf import settings
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


def get_user_display_name(user, fallback="Un autre utilisateur"):
    """
    Returns the human-friendly display name for a user:
    1. Full name (first_name + last_name) if available via user.get_full_name()
    2. Email address if available
    3. Username if available
    4. Provided fallback string or None
    """
    if not user:
        return fallback if fallback != "Un autre utilisateur" else None
    full_name = user.get_full_name() if hasattr(user, "get_full_name") else ""
    return full_name or getattr(user, "email", "") or getattr(user, "username", "") or fallback


class TeamAutoCreationExclusion(TimeStampedModel):
    """
    SIREN numbers excluded from automatic Team creation and pooling
    during ProConnect authentication (e.g. national police, ministries, headquarters).
    Users with these identifiers remain in individual mode.
    """

    siren = models.CharField("SIREN", max_length=9, unique=True, db_index=True)
    label = models.CharField("Nom de l'organisme / Direction", max_length=255)
    reason = models.TextField("Motif de l'exclusion", blank=True)

    class Meta:
        verbose_name = "exclusion d'auto-création d'équipe"
        verbose_name_plural = "exclusions d'auto-création d'équipe"

    def __str__(self):
        return f"{self.label} ({self.siren})"

    @classmethod
    def is_excluded(cls, siren):
        clean_siren = (siren or "").strip()[:9]
        if not clean_siren:
            return False
        return cls.objects.filter(siren=clean_siren).exists()
