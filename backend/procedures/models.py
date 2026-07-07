from django.conf import settings
from django.db import models
from model_utils.fields import MonitorField
from model_utils.models import TimeStampedModel


class SuiviProcedure(TimeStampedModel):
    constatation = models.OneToOneField(
        "constatations.Constatation",
        on_delete=models.CASCADE,
        related_name="suivi_procedure",
        verbose_name="Constatation liée",
        null=True,
        blank=True,
    )
    etape_en_cours = models.PositiveSmallIntegerField(default=1, verbose_name="Étape active")
    preuves_fournies = models.BooleanField(default=False, verbose_name="Éléments de preuve joints")
    constatation_signee = models.BooleanField(
        default=False, verbose_name="Rapport de constatation signé"
    )
    lettre_signe = models.BooleanField(default=False, verbose_name="Lettre d'information signée")
    identification_reussie = models.BooleanField(
        null=True, blank=True, verbose_name="Identification de l'auteur réussie"
    )
    lettre_envoyee = models.BooleanField(default=False, verbose_name="Lettre d'information envoyée")
    lettre_envoyee_date = models.DateField(
        null=True, blank=True, verbose_name="Date d'envoi de la lettre"
    )
    copie_archives = models.BooleanField(default=False, verbose_name="Copie archivée")
    ar_recu = models.BooleanField(default=False, verbose_name="Accusé de réception reçu")
    ar_statut = models.CharField(max_length=20, blank=True, verbose_name="Statut de l'AR")
    ar_presentation_date = models.DateField(
        null=True, blank=True, verbose_name="Date de présentation de l'AR"
    )
    decision_poursuite = models.CharField(
        max_length=50, blank=True, verbose_name="Décision de poursuite"
    )
    montant_fixe = models.BooleanField(default=False, verbose_name="Montant fixé")
    montant_amende = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Montant de l'amende"
    )
    arrete_redige = models.BooleanField(default=False, verbose_name="Arrêté rédigé")
    titre_recette_emis = models.BooleanField(default=False, verbose_name="Titre de recette émis")
    notification_sanction_envoyee = models.BooleanField(
        default=False, verbose_name="Notification de sanction envoyée"
    )
    motif_abandon = models.CharField(max_length=255, blank=True, verbose_name="Motif d'abandon")
    souhaite_notifier_abandon = models.BooleanField(
        null=True, blank=True, verbose_name="Souhaite notifier l'abandon"
    )
    notification_abandon_envoyee = models.BooleanField(
        default=False, verbose_name="Notification d'abandon envoyée"
    )
    nettoyage_fait = models.BooleanField(null=True, blank=True, verbose_name="Nettoyage effectué")
    nettoyage_par = models.CharField(
        max_length=255, blank=True, verbose_name="Nettoyage effectué par"
    )
    date_recouvrement_effective = models.DateField(
        null=True, blank=True, verbose_name="Date de recouvrement effective"
    )
    titre_recette_confirme = models.BooleanField(
        default=False, verbose_name="Titre de recette confirmé"
    )
    montant_recouvre = models.BooleanField(default=False, verbose_name="Montant recouvré")
    dossier_archive = models.BooleanField(default=False, verbose_name="Dossier archivé")
    # Backoffice
    observations_internes = models.TextField(blank=True, verbose_name="Observations internes")
    statut_traitement = models.CharField(
        max_length=20,
        default="Nouveau",
        verbose_name="Statut de traitement",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"is_staff": True},
        related_name="assigned_suivi_procedures",
        verbose_name="Assigné à",
    )
    assigned_at = MonitorField(
        monitor="assigned_to",
        null=True,
        blank=True,
        verbose_name="Date d'assignation",
    )

    class Meta:
        verbose_name = "Suivi de procédure"
        verbose_name_plural = "Suivis de procédures"

    def __str__(self):
        return f"Suivi {self.constatation_id or self.id}"
