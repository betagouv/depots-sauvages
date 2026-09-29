from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel
from solo.models import SingletonModel


class ProConnectAccessConfig(SingletonModel):
    categories_juridiques_autorisees = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Catégories juridiques autorisées",
        help_text="Liste JSON des catégories autorisées (ex: [{'code': '72', 'nom': 'Communes...'}])",
    )
    sirens_autorises = models.JSONField(
        default=list,
        blank=True,
        verbose_name="SIREN autorisés (liste blanche)",
        help_text="Liste JSON des SIREN spécifiquement autorisés (ex: [{'siren': '157000019', 'nom': 'Gendarmerie...'}])",
    )

    class Meta:
        verbose_name = "Configuration d'accès ProConnect"

    def __str__(self):
        return "Configuration d'accès ProConnect"

    def est_siren_autorise(self, siren: str) -> bool:
        if not siren:
            return False
        clean_siren = str(siren).strip()
        sirens = [
            str(item.get("siren") if isinstance(item, dict) else item).strip()
            for item in (self.sirens_autorises or [])
        ]
        return clean_siren in sirens

    def est_categorie_juridique_autorisee(self, categorie_juridique: str) -> bool:
        if not categorie_juridique:
            return False
        clean_cat = str(categorie_juridique).strip()
        prefixes = tuple(
            p
            for p in (
                str(item.get("code") if isinstance(item, dict) else item).strip()
                for item in (self.categories_juridiques_autorisees or [])
            )
            if p
        )
        if not prefixes:
            return False
        return clean_cat.startswith(prefixes)


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
