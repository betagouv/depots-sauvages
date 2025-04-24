from django.db import models


class Signalement(models.Model):
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
    types_depot = models.JSONField("types", default=list, blank=True, null=True)
    precisions_depot = models.TextField("précisions", blank=True)
    photo_dispo = models.BooleanField("photos", default=False)
    auteur_identifie = models.BooleanField("identifié", default=False)
    souhaite_porter_plainte = models.BooleanField("plainte", default=False)
    indices_disponibles = models.JSONField("indices", default=list, blank=True, null=True)
    precisions_indices = models.TextField("précisions indices", blank=True)
    arrete_municipal_existe = models.BooleanField("arrêté", default=False)
    prejudice_montant_connu = models.BooleanField("montant connu", default=False)
    prejudice_montant = models.IntegerField("montant", null=True, blank=True)
    prejudice_nombre_personnes = models.IntegerField("personnes", null=True, blank=True)
    prejudice_nombre_heures = models.IntegerField("heures", null=True, blank=True)
    prejudice_nombre_vehicules = models.IntegerField("véhicules", null=True, blank=True)
    prejudice_kilometrage = models.IntegerField("kilométrage", null=True, blank=True)
    prejudice_autres_couts = models.IntegerField("autres coûts", null=True, blank=True)
    document = models.BinaryField("Document généré", null=True, blank=True)
    # Management fields
    generate_doc = models.BooleanField(
        "Générer le document",
        default=False,
        help_text="Flag indicating if document should be generated",
    )
    document_generated_at = models.DateTimeField("Date de génération", null=True, blank=True)

    def get_prejudice_montant_calcule(self):
        """
        Calculate the total amount of prejudice, when the amount is unknown.
        """
        if self.prejudice_montant_connu:
            # If the amount is known, return the amount.
            # This should not happen, but it's a safety net.
            return self.prejudice_montant
        AGENT_HOURLY_RATE = 18.03  # In euros, the hourly rate of a person
        VEHICLE_USAGE_RATE = 1.30  # In euros, the usage rate of a vehicle
        agent_cost = self.prejudice_nombre_personnes * AGENT_HOURLY_RATE
        total_agent_cost = agent_cost * self.prejudice_nombre_heures
        vehicle_cost = self.prejudice_kilometrage * VEHICLE_USAGE_RATE
        total_vehicle_cost = vehicle_cost * self.prejudice_nombre_vehicules
        total_cost = total_agent_cost + total_vehicle_cost
        return total_cost

    class Meta:
        verbose_name = "signalement"
        verbose_name_plural = "signalements"

    def __str__(self):
        return f"Dépôt à {self.commune} le {self.date_constat}"
