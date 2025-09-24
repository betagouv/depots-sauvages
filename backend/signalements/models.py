import logging

from django.db import models
from django.template.loader import render_to_string
from model_utils.models import TimeStampedModel

from backend.email_sending.handlers import EmailHandler
from backend.signalements.prejudice import PrejudiceMixin

logger = logging.getLogger(__name__)


class Signalement(PrejudiceMixin, TimeStampedModel):
    """
    Model for waste deposit reports
    """

    commune = models.CharField("commune", max_length=255)
    localisation_depot = models.CharField("localisation", max_length=255, blank=True)
    date_constat = models.DateField("date de constatation")
    heure_constat = models.TimeField("heure de constatation")
    auteur_signalement = models.CharField("auteur signalement", max_length=255, blank=True)
    nature_terrain = models.JSONField("terrain", default=list, blank=True, null=True)
    volume_depot = models.CharField("volume", max_length=255, blank=True)
    risque_ecoulement = models.BooleanField("risque d'écoulement", default=False)
    types_depot = models.JSONField("types", default=list, blank=True, null=True)
    precisions_depot = models.TextField("précisions", blank=True)
    photo_dispo = models.BooleanField("photos", default=False)
    auteur_identifie = models.BooleanField("auteur identifié", default=False)
    souhaite_porter_plainte = models.BooleanField("souhaite porter plainte", default=False)
    indices_disponibles = models.JSONField("indices", default=list, blank=True, null=True)
    precisions_indices = models.TextField("précisions indices", blank=True)
    arrete_municipal_existe = models.BooleanField("arrêté municipal existe", default=False)
    montant_forfait_enlevement = models.IntegerField("forfait enlèvement", null=True, blank=True)
    prejudice_montant_connu = models.BooleanField("montant connu", default=False)
    prejudice_montant = models.IntegerField("montant préjudice", null=True, blank=True)
    prejudice_nombre_personnes = models.IntegerField("personnes", null=True, blank=True)
    prejudice_nombre_heures = models.IntegerField("heures", null=True, blank=True)
    prejudice_nombre_vehicules = models.IntegerField("véhicules", null=True, blank=True)
    prejudice_kilometrage = models.IntegerField("kilométrage", null=True, blank=True)
    prejudice_autres_couts = models.IntegerField("autres coûts", null=True, blank=True)
    prenom_particulier = models.CharField("prénom du particulier", max_length=255, blank=True)
    nom_particulier = models.CharField("nom du particulier", max_length=255, blank=True)
    nom_entreprise = models.CharField("nom de l'entreprise", max_length=255, blank=True)
    numero_siret = models.CharField("numéro SIRET", max_length=255, blank=True)
    statut_auteur = models.CharField("statut de l'auteur", max_length=255, null=True, blank=True)
    contact_nom = models.CharField("nom du contact", max_length=255, blank=True)
    contact_prenom = models.CharField("prénom du contact", max_length=255, blank=True)
    contact_email = models.EmailField("email du contact", blank=True)
    contact_telephone = models.CharField("téléphone du contact", max_length=20, blank=True)
    accepte_accompagnement = models.BooleanField("accepte accompagnement", default=False)
    # Documents fields
    doc_constat = models.BinaryField("Rapport de constatation", null=True, blank=True)
    lettre_info = models.BinaryField("Lettre d'information", null=True, blank=True)
    # Management fields
    doc_constat_should_generate = models.BooleanField(
        "Générer le rapport de constatation",
        default=False,
        help_text="Faut-il générer le rapport de constatation ?",
    )
    doc_constat_generated_at = models.DateTimeField(
        "date rapport de constatation", null=True, blank=True
    )
    lettre_info_should_generate = models.BooleanField(
        "Générer la lettre d'information",
        default=False,
        help_text="Faut-il générer la lettre d'information ?",
    )
    lettre_info_generated_at = models.DateTimeField(
        "date lettre information", null=True, blank=True
    )

    class Meta:
        verbose_name = "signalement"
        verbose_name_plural = "signalements"

    def __str__(self):
        return f"Dépôt à {self.commune} le {self.date_constat}"

    def send_contact_person_email(self):
        """
        Send email to contact person with signalement documents.
        """
        if not self.contact_email:
            raise ValueError("Contact email is required")
        self.refresh_from_db()  # Get latest document data
        subject = f"Documents du signalement #{self.id} - {self.commune}"
        html_template = render_to_string("email-get-documents.html", {"signalement": self})
        handler = EmailHandler(
            subject=subject, html_template=html_template, to_emails=[self.contact_email]
        )
        logger.info(f"Sending email for signalement {self.id}")
        if not self.doc_constat:
            logger.warning(
                f"Missing doc_constat for signalement {self.id} - "
                f"email will be sent without rapport de constatation"
            )
        if not self.lettre_info:
            logger.warning(
                f"Missing lettre_info for signalement {self.id} - "
                f"email will be sent without lettre d'information"
            )
        if self.doc_constat:
            handler.add_attachment(
                filename=f"rapport-constatation-{self.id}-{self.commune}.odt",
                content=self.doc_constat,
                mimetype="application/vnd.oasis.opendocument.text",
            )
        if self.lettre_info:
            handler.add_attachment(
                filename=f"lettre-info-{self.id}-{self.commune}.odt",
                content=self.lettre_info,
                mimetype="application/vnd.oasis.opendocument.text",
            )
        return handler.send()
