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

    stats_exclude = {"doc_constat", "lettre_info", "photos"}
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


class ExternalMetric(TrackingBaseModel):
    """Agrégat journalier issu d'une source externe (Matomo, Tally, RDV Service Public).

    Une ligne = un jour, une métrique, une modalité, et le nombre d'occurrences.

    Deux règles structurent ce modèle :

    1. On ne stocke jamais de réponse individuelle ni de donnée personnelle. Les
       collecteurs (`backend/stats/collectors/`) interrogent les API, comptent, et
       jettent le détail.
    2. On ne stocke jamais de taux ni de moyenne pré-calculés. Une moyenne de moyennes
       journalières est fausse dès que le nombre de réponses varie d'un jour à l'autre.
       En gardant les effectifs, Metabase recalcule la valeur exacte sur n'importe
       quelle période : `SUM(dimension * value) / SUM(value)`.
    """

    class Source(models.TextChoices):
        MATOMO = "matomo", "Matomo"
        TALLY = "tally", "Tally"
        RDV = "rdv", "RDV Service Public"

    source = models.CharField("source", max_length=20, choices=Source.choices)
    metric = models.CharField("métrique", max_length=64)
    date = models.DateField("jour")
    dimension = models.CharField("modalité", max_length=128, blank=True, default="")
    value = models.DecimalField("valeur", max_digits=14, decimal_places=2)
    details = models.JSONField("détails", default=dict, blank=True)
    collected_at = models.DateTimeField("collecté le", auto_now=True)

    class Meta:
        db_table = "stats_external_metric"
        verbose_name = "Métrique externe"
        verbose_name_plural = "Métriques externes"
        constraints = [
            models.UniqueConstraint(
                fields=["source", "metric", "date", "dimension"],
                name="unique_external_metric",
            )
        ]
        indexes = [
            models.Index(fields=["source", "metric", "date"], name="external_metric_lookup_idx"),
        ]

    def __str__(self):
        return f"{self.date} {self.source}.{self.metric}[{self.dimension}] = {self.value}"
