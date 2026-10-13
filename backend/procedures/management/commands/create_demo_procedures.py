from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from backend.constatations.models import Constatation

# Pre-checked procedure steps reused to compose test scenarios
SIGNE = {"preuves_fournies": True, "constatation_signee": True, "lettre_signe": True}
ENVOYE = {**SIGNE, "lettre_envoyee": True, "copie_archives": True}
SANCTION_FAITE = {
    "decision_poursuite": "sanction",
    "montant_fixe": True,
    "arrete_redige": True,
    "titre_recette_emis": True,
    "notification_sanction_envoyee": True,
}


def scenarios():
    """
    Mock cases covering every column of the "Mes procédures" dashboard.
    Dates are defined in days before today so deadlines (especially contradictory periods)
    remain meaningful whenever tests or demos are executed.
    """
    return [
        {"commune": "Nangy", "constat": 2, "is_draft": True, "auteur_identifie": None},
        {"commune": "Nangy", "constat": 20, "auteur_identifie": False, "suivi": {}},
        {"nom": "Martin", "prenom": "Lucie", "commune": "Arthaz-Pont-Notre-Dame", "constat": 4},
        {
            "nom": "Bernard",
            "prenom": "Sophie",
            "commune": "Reignier-Ésery",
            "constat": 9,
            "suivi": {"preuves_fournies": True, "constatation_signee": True},
        },
        # Incomplete workflow edge case: decision taken without signed documents
        {
            "nom": "Chevalier",
            "prenom": "Paul",
            "commune": "Reignier-Ésery",
            "constat": 60,
            "suivi": {"decision_poursuite": "sanction", "lettre_envoyee": True},
        },
        {"nom": "Petit", "prenom": "Antoine", "commune": "Reignier-Ésery", "constat": 8, "suivi": SIGNE},
        {
            "nom": "Bâti Express SARL",
            "statut_auteur": "entreprise",
            "commune": "Nangy",
            "constat": 12,
            "suivi": SIGNE,
        },
        {
            "nom": "Durand",
            "prenom": "Pierre",
            "commune": "Arthaz-Pont-Notre-Dame",
            "constat": 15,
            "suivi": {**ENVOYE, "lettre_envoyee_date": 5},
        },
        {
            "nom": "Leroy",
            "prenom": "Julie",
            "commune": "Reignier-Ésery",
            "constat": 20,
            "suivi": {
                **ENVOYE,
                "lettre_envoyee_date": 6,
                "ar_recu": True,
                "ar_statut": "distribue",
                "ar_presentation_date": 3,
            },
        },
        {
            "nom": "Moreau",
            "prenom": "Karim",
            "commune": "Nangy",
            "constat": 22,
            "suivi": {
                **ENVOYE,
                "lettre_envoyee_date": 10,
                "ar_recu": True,
                "ar_statut": "non_reclame",
                "ar_presentation_date": 7,
            },
        },
        # Contradictory ended, but copy to archives is unchecked
        {
            "nom": "Fournier",
            "prenom": "Claire",
            "commune": "Reignier-Ésery",
            "constat": 35,
            "suivi": {
                **ENVOYE,
                "copie_archives": False,
                "lettre_envoyee_date": 24,
                "ar_recu": True,
                "ar_statut": "distribue",
                "ar_presentation_date": 20,
            },
        },
        {
            "nom": "Dupont",
            "prenom": "Marc",
            "commune": "Reignier-Ésery",
            "constat": 40,
            "suivi": {
                **ENVOYE,
                "lettre_envoyee_date": 30,
                "ar_recu": True,
                "ar_statut": "distribue",
                "ar_presentation_date": 25,
            },
        },
        {
            "nom": "Lambert",
            "prenom": "Hugo",
            "commune": "Arthaz-Pont-Notre-Dame",
            "constat": 45,
            "suivi": {**ENVOYE, "lettre_envoyee_date": 35, "ar_recu": True, "ar_statut": "npai"},
        },
        {
            "nom": "Girard",
            "prenom": "Emma",
            "commune": "Nangy",
            "constat": 50,
            "suivi": {
                **ENVOYE,
                "lettre_envoyee_date": 40,
                "ar_recu": True,
                "ar_statut": "npai",
                "decision_poursuite": "recherche_adresse",
            },
        },
        {
            "nom": "Roux",
            "prenom": "Thomas",
            "commune": "Reignier-Ésery",
            "constat": 55,
            "suivi": {
                **ENVOYE,
                "lettre_envoyee_date": 45,
                "ar_recu": True,
                "ar_statut": "distribue",
                "ar_presentation_date": 42,
                "decision_poursuite": "sanction",
                "montant_fixe": True,
                "montant_amende": Decimal("500"),
            },
        },
        {
            "nom": "Garnier",
            "prenom": "Léa",
            "commune": "Arthaz-Pont-Notre-Dame",
            "constat": 58,
            "suivi": {
                **ENVOYE,
                "lettre_envoyee_date": 48,
                "ar_recu": True,
                "ar_statut": "distribue",
                "ar_presentation_date": 46,
                "decision_poursuite": "abandon",
            },
        },
        {
            "nom": "Faure",
            "prenom": "Nicolas",
            "commune": "Nangy",
            "constat": 90,
            "suivi": {
                **ENVOYE,
                "lettre_envoyee_date": 80,
                "ar_recu": True,
                "ar_statut": "distribue",
                "ar_presentation_date": 78,
                "decision_poursuite": "abandon",
                "motif_abandon": "Indulgence : le contrevenant a nettoyé le dépôt",
                "souhaite_notifier_abandon": False,
            },
        },
        {
            "nom": "Mercier",
            "prenom": "Julien",
            "commune": "Reignier-Ésery",
            "constat": 100,
            "suivi": {
                **ENVOYE,
                **SANCTION_FAITE,
                "lettre_envoyee_date": 90,
                "ar_recu": True,
                "ar_statut": "distribue",
                "ar_presentation_date": 88,
                "montant_amende": Decimal("300"),
            },
        },
        {
            "nom": "Blanc",
            "prenom": "Sarah",
            "commune": "Arthaz-Pont-Notre-Dame",
            "constat": 150,
            "suivi": {
                **ENVOYE,
                **SANCTION_FAITE,
                "lettre_envoyee_date": 140,
                "ar_recu": True,
                "ar_statut": "distribue",
                "ar_presentation_date": 137,
                "montant_amende": Decimal("1500"),
                "titre_recette_confirme": True,
                "montant_recouvre": True,
                "date_recouvrement_effective": 30,
                "dossier_archive": True,
            },
        },
        {
            "commune": "Nangy",
            "constat": 120,
            "auteur_identifie": False,
            "suivi": {
                "preuves_fournies": True,
                "constatation_signee": True,
                "identification_reussie": False,
                "dossier_archive": True,
            },
        },
    ]


DATE_FIELDS = ("lettre_envoyee_date", "ar_presentation_date", "date_recouvrement_effective")

# Varied dump site locations, matching typical free-text entries
LIEUX = (
    "Chemin des Saules, près du point d'apport volontaire",
    "Route de Nangy",
    "Parking du stade",
    "Bord du Foron, sous le pont de la D903, derrière le local technique de l'association",
    "Lieu-dit Les Granges",
    "Rue de la Mairie",
    "Forêt communale, chemin forestier n°3",
)


class Command(BaseCommand):
    help = (
        "Crée des dossiers fictifs pour tester le tableau de bord « Mes procédures » en local. "
        "Refuse de tourner en production."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            required=True,
            help="Adresse de connexion du compte de démo (créé s'il n'existe pas).",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Supprime d'abord les dossiers de démo déjà créés pour ce compte.",
        )

    def handle(self, *args, **options):
        env_name = getattr(settings, "ENV_NAME", "").lower()
        if "prod" in env_name:
            raise CommandError("Commande interdite en production.")
        email = options["email"].strip().lower()
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=email,
            defaults={"email": email, "first_name": "Compte", "last_name": "Démo"},
        )
        if user.is_staff or user.is_superuser:
            raise CommandError("Le compte de démo ne doit pas être un compte administrateur.")
        today = timezone.localdate()
        with transaction.atomic():
            if options["reset"]:
                deleted, _ = Constatation.objects.filter(user=user, ceci_est_un_test=True).delete()
                self.stdout.write(f"{deleted} objets de démo supprimés.")
            for index, scenario in enumerate(scenarios()):
                self.create_dossier(user, scenario, today, LIEUX[index % len(LIEUX)])
        self.stdout.write(
            self.style.SUCCESS(
                f"{len(scenarios())} dossiers de démo créés pour {email}"
                f"{' (compte créé)' if created else ''}."
            )
        )

    def create_dossier(self, user, scenario, today, lieu):
        auteur_identifie = scenario.get("auteur_identifie", True)
        constatation = Constatation.objects.create(
            user=user,
            ceci_est_un_test=True,
            is_draft=scenario.get("is_draft", False),
            commune=scenario["commune"],
            localisation_depot=lieu,
            date_constat=today - timedelta(days=scenario["constat"]),
            auteur_identifie=auteur_identifie,
            statut_auteur=scenario.get(
                "statut_auteur", "particulier" if auteur_identifie else None
            ),
            auteur_nom=scenario.get("nom", ""),
            auteur_prenom=scenario.get("prenom", ""),
            precisions_depot="Dossier fictif de démonstration",
        )
        suivi = constatation.suivi_procedure
        for field, value in scenario.get("suivi", {}).items():
            if field in DATE_FIELDS:
                value = today - timedelta(days=value)
            setattr(suivi, field, value)
        suivi.save()
