from django.db import models
from model_utils.models import TimeStampedModel


class SuiviProcedure(TimeStampedModel):
    signalement = models.OneToOneField(
        "dn_signalements.DNSignalement",
        on_delete=models.CASCADE,
        related_name="suivi_procedure",
        verbose_name="Signalement lié",
    )
    etape_en_cours = models.PositiveSmallIntegerField(default=1, verbose_name="Étape active")
    # Étape 1 : Pièces de procédure
    preuves_fournies = models.BooleanField(default=False, verbose_name="Éléments de preuve joints")
    constatation_signee = models.BooleanField(
        default=False, verbose_name="Rapport de constatation signé"
    )
    lettre_signe = models.BooleanField(default=False, verbose_name="Lettre d'information signée")
    # Étape 2 : Notification
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
    # Étape 4 : Actions selon décision
    decision_poursuite = models.CharField(
        max_length=50, blank=True, verbose_name="Décision de poursuite"
    )
    # - Si Sanction
    montant_fixe = models.BooleanField(default=False, verbose_name="Montant fixé")
    montant_amende = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Montant de l'amende"
    )
    arrete_redige = models.BooleanField(default=False, verbose_name="Arrêté rédigé")
    titre_recette_emis = models.BooleanField(default=False, verbose_name="Titre de recette émis")
    notification_sanction_envoyee = models.BooleanField(
        default=False, verbose_name="Notification de sanction envoyée"
    )
    # - Si Abandon
    motif_abandon_choisi = models.BooleanField(default=False, verbose_name="Motif d'abandon choisi")
    motif_abandon = models.CharField(max_length=255, blank=True, verbose_name="Motif d'abandon")
    souhaite_notifier_abandon = models.BooleanField(
        null=True, blank=True, verbose_name="Souhaite notifier l'abandon"
    )
    notification_abandon_envoyee = models.BooleanField(
        default=False, verbose_name="Notification d'abandon envoyée"
    )
    # Infos Complémentaires / Étape 5
    nettoyage_fait = models.BooleanField(null=True, blank=True, verbose_name="Nettoyage effectué")
    nettoyage_par = models.CharField(
        max_length=255, blank=True, verbose_name="Nettoyage effectué par"
    )
    observations_internes = models.TextField(blank=True, verbose_name="Observations internes")

    date_recouvrement_effective = models.DateField(
        null=True, blank=True, verbose_name="Date de recouvrement effective"
    )
    titre_recette_confirme = models.BooleanField(
        default=False, verbose_name="Titre de recette confirmé"
    )
    montant_recouvre = models.BooleanField(default=False, verbose_name="Montant recouvré")
    dossier_archive = models.BooleanField(default=False, verbose_name="Dossier archivé")

    class Meta:
        verbose_name = "Suivi de procédure"
        verbose_name_plural = "Suivis de procédures"

    def __str__(self):
        return f"Suivi {self.signalement_id}"
