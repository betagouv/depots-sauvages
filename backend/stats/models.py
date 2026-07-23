from django.db import models
from trackman.models import TrackingBaseModel

from backend.constatations.models import ConstatationBaseModel
from backend.procedures.models import SuiviProcedureBaseModel
from backend.stats.anonymizer import (
    anonymize_email,
    anonymize_fake_name,
    anonymize_phone,
    anonymize_text,
    anonymize_user_hash,
)


class StatsConstatation(ConstatationBaseModel, TrackingBaseModel):
    user_hash = models.CharField("hash utilisateur", max_length=64, blank=True, null=True)

    stats_exclude = {"doc_constat", "lettre_info"}
    stats_anonymize = {
        "user_hash": anonymize_user_hash,
        "constatant_nom": anonymize_fake_name,
        "constatant_prenom": anonymize_fake_name,
        "contact_nom": anonymize_fake_name,
        "contact_prenom": anonymize_fake_name,
        "contact_email": anonymize_email,
        "contact_telephone": anonymize_phone,
        "auteur_nom": anonymize_fake_name,
        "auteur_prenom": anonymize_fake_name,
        "auteur_adresse": anonymize_text,
        "proprietaire_terrain_prive": anonymize_text,
    }

    class Meta:
        db_table = "stats_constatation"
        verbose_name = "Statistique Constatation"
        verbose_name_plural = "Statistiques Constatations"


class StatsSuiviProcedure(SuiviProcedureBaseModel, TrackingBaseModel):
    constatation = models.OneToOneField(
        StatsConstatation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="suivi_procedure",
    )
    personne_assignee_id = models.IntegerField(null=True, blank=True)

    stats_exclude = set()
    stats_anonymize = {
        "observations_internes": anonymize_text,
        "notes_traitement": anonymize_text,
    }

    class Meta:
        db_table = "stats_suivi_procedure"
        verbose_name = "Statistique Suivi de procédure"
        verbose_name_plural = "Statistiques Suivis de procédures"
