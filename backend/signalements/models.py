from django.db import models

from backend.signalements.prejudice import PrejudiceMixin


class Signalement(PrejudiceMixin, models.Model):
    """
    Model for waste deposit reports
    """

    commune = models.CharField("commune", max_length=255)
    localisation_depot = models.CharField("localisation", max_length=255, blank=True)
    date_constat = models.DateField("date")
    heure_constat = models.TimeField("heure")
    auteur_signalement = models.CharField("auteur", max_length=255, blank=True)
    nature_terrain = models.CharField("terrain", max_length=255, blank=True)
    volume_depot = models.CharField("volume", max_length=255, blank=True)
    risque_ecoulement = models.BooleanField("risque d'écoulement", default=False)
    types_depot = models.JSONField("types", default=list, blank=True, null=True)
    precisions_depot = models.TextField("précisions", blank=True)
    photo_dispo = models.BooleanField("photos", default=False)
    auteur_identifie = models.BooleanField("identifié", default=False)
    souhaite_porter_plainte = models.BooleanField("plainte", default=False)
    indices_disponibles = models.JSONField("indices", default=list, blank=True, null=True)
    precisions_indices = models.TextField("précisions indices", blank=True)
    arrete_municipal_existe = models.BooleanField("arrêté", default=False)
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
    document = models.BinaryField("Document généré", null=True, blank=True)
    # Management fields
    generate_doc = models.BooleanField(
        "Générer le document",
        default=False,
        help_text="Flag indicating if document should be generated",
    )
    document_generated_at = models.DateTimeField("Date de génération", null=True, blank=True)

    class Meta:
        verbose_name = "signalement"
        verbose_name_plural = "signalements"

    def __str__(self):
        return f"Dépôt à {self.commune} le {self.date_constat}"
