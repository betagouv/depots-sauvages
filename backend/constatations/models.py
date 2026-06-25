from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel

from backend.constatations.prejudice import PrejudiceMixin


class Constatation(PrejudiceMixin, TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="constatations",
        null=True,
        blank=True,
    )
    commune = models.CharField("commune", max_length=255)
    localisation_depot = models.TextField("localisation", blank=True)
    date_constat = models.DateField("date de constatation", null=True, blank=True)
    heure_constat = models.TimeField("heure de constatation", null=True, blank=True)
    constatant_civilite = models.CharField("civilité du constatant", max_length=255, blank=True)
    constatant_role = models.CharField("rôle du constatant", max_length=255, blank=True)
    constatant_nom = models.CharField("nom du constatant", max_length=255, blank=True)
    constatant_prenom = models.CharField("prénom du constatant", max_length=255, blank=True)
    constatant_est_utilisateur_connecte = models.BooleanField(
        "Le constatant est l'utilisateur connecté", default=True
    )
    nature_terrain = models.JSONField("terrain", default=list, blank=True, null=True)
    proprietaire_terrain_prive = models.CharField(
        "propriétaire terrain privé", max_length=255, blank=True
    )

    volume_depot = models.CharField("volume", max_length=255, blank=True)
    types_depot = models.JSONField("types", default=list, blank=True, null=True)
    precisions_depot = models.TextField("précisions", blank=True)
    photo_dispo = models.BooleanField("photos", default=False)
    risque_ecoulement = models.BooleanField("risque écoulement", default=False)

    auteur_identifie = models.BooleanField("auteur présumé identifié", default=False)
    statut_auteur = models.CharField(
        "statut de l'auteur présumé", max_length=255, null=True, blank=True
    )
    auteur_civilite = models.CharField("civilité de l'auteur présumé", max_length=255, blank=True)
    auteur_nom = models.CharField("nom de l'auteur présumé", max_length=255, blank=True)
    auteur_prenom = models.CharField("prénom de l'auteur présumé", max_length=255, blank=True)
    auteur_adresse = models.TextField("adresse de l'auteur présumé", blank=True)
    auteur_siret = models.CharField("siret de l'auteur présumé", max_length=255, blank=True)
    entreprise_francaise = models.BooleanField("entreprise française", null=True, blank=True)
    informations_auteur = models.JSONField(
        "informations auteur présumé", default=list, blank=True, null=True
    )
    plainte_etat = models.CharField("état de la plainte", max_length=255, blank=True)
    indices_disponibles = models.JSONField("indices", default=list, blank=True, null=True)
    precisions_indices = models.TextField("précisions indices", blank=True)

    prejudice_montant_connu = models.BooleanField("montant connu", default=False)
    prejudice_montant = models.FloatField("montant préjudice", null=True, blank=True)
    prejudice_nombre_personnes = models.FloatField("personnes", null=True, blank=True)
    prejudice_nombre_heures = models.FloatField("heures", null=True, blank=True)
    prejudice_nombre_vehicules = models.FloatField("véhicules", null=True, blank=True)
    prejudice_kilometrage = models.FloatField("kilométrage", null=True, blank=True)
    prejudice_autres_couts = models.FloatField("autres coûts", null=True, blank=True)

    contact_nom = models.CharField("nom du contact", max_length=255, blank=True)
    contact_prenom = models.CharField("prénom du contact", max_length=255, blank=True)
    contact_email = models.EmailField("email du contact", blank=True)
    contact_telephone = models.CharField("téléphone du contact", max_length=255, blank=True)
    accepte_accompagnement = models.BooleanField("accepte accompagnement", default=False)
    ceci_est_un_test = models.BooleanField("est un test", null=True, blank=True)

    # Documents fields
    doc_constat = models.BinaryField("Rapport de constatation", null=True, blank=True)
    lettre_info = models.BinaryField("Lettre d'information", null=True, blank=True)

    # Management fields
    doc_constat_should_generate = models.BooleanField(
        "Générer le rapport de constatation",
        default=False,
    )
    doc_constat_generated_at = models.DateTimeField(
        "date rapport de constatation", null=True, blank=True
    )
    lettre_info_should_generate = models.BooleanField(
        "Générer la lettre d'information",
        default=False,
    )
    lettre_info_generated_at = models.DateTimeField(
        "date lettre information", null=True, blank=True
    )

    class Meta:
        verbose_name = "constatation"
        verbose_name_plural = "constatations"

    @property
    def souhaite_porter_plainte(self):
        """
        Property for backward compatibility with document templates.
        Returns True if a complaint is filed or planned.
        """
        return self.plainte_etat in ["Déposée", "Sera déposée"]

    def save(self, *args, **kwargs):
        if self.souhaite_porter_plainte:
            if not self.prejudice_montant_connu:
                self.prejudice_montant = self.get_prejudice_montant_calcule()
        else:
            self.prejudice_montant_connu = False
            self.prejudice_montant = None
            self.prejudice_nombre_personnes = None
            self.prejudice_nombre_heures = None
            self.prejudice_nombre_vehicules = None
            self.prejudice_kilometrage = None
            self.prejudice_autres_couts = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Constatation à {self.commune} ({self.date_constat})"
