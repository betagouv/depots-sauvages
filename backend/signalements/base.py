from django.db import models


class AbstractSignalementBase(models.Model):
    """
    Abstract base model containing all common signalement fields.
    """

    commune = models.CharField("commune", max_length=255)
    localisation_depot = models.CharField("localisation", max_length=255, blank=True)
    date_constat = models.DateField("date de constatation")
    heure_constat = models.TimeField("heure de constatation")
    constatant = models.CharField("constatant", max_length=255, blank=True)
    nature_terrain = models.JSONField("terrain", default=list, blank=True, null=True)
    volume_depot = models.CharField("volume", max_length=255, blank=True)
    types_depot = models.JSONField("types", default=list, blank=True, null=True)
    precisions_depot = models.TextField("précisions", blank=True)
    photo_dispo = models.BooleanField("photos", default=False)
    auteur_identifie = models.BooleanField("auteur identifié", default=False)
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
        abstract = True
