from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from backend.constatations.models import Constatation
from backend.teams.models import Team, UserProfile

SIGNE = {"preuves_fournies": True, "constatation_signee": True, "lettre_signe": True}
ENVOYE = {**SIGNE, "lettre_envoyee": True, "copie_archives": True}
SANCTION = {
    "decision_poursuite": "sanction",
    "montant_fixe": True,
    "arrete_redige": True,
    "titre_recette_emis": True,
    "notification_sanction_envoyee": True,
}


class Command(BaseCommand):
    help = (
        "Initialise un jeu complet d'utilisateurs et de dossiers multi-équipes pour la démo/test."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset", action="store_true", help="Supprime d'abord les données des comptes démo."
        )

    def handle(self, *args, **options):
        env_name = getattr(settings, "ENV_NAME", "").lower()
        if "prod" in env_name:
            raise CommandError("Commande strictement interdite en production.")

        User = get_user_model()
        today = timezone.localdate()

        demo_emails = [
            "agent1.reignier@demo.fr",
            "agent2.reignier@demo.fr",
            "agent1.nangy@demo.fr",
            "gendarme1@demo.fr",
            "gendarme2@demo.fr",
            "admin@demo.fr",
        ]

        with transaction.atomic():
            if options["reset"]:
                Constatation.objects.filter(created_by__username__in=demo_emails).delete()
                Team.objects.filter(siret__in=["21740220600010", "21740198400013"]).delete()
                User.objects.filter(username__in=demo_emails).delete()
                self.stdout.write("Anciennes données démo supprimées.")

            # 1. Équipe Commune de Reignier-Ésery
            team_reignier, _ = Team.objects.get_or_create(
                siret="21740220600010",
                defaults={"name": "Mairie de Reignier-Ésery", "siren": "217402206"},
            )
            u_r1, _ = User.objects.get_or_create(
                username="agent1.reignier@demo.fr",
                defaults={
                    "email": "agent1.reignier@demo.fr",
                    "first_name": "Marc",
                    "last_name": "Dubois",
                },
            )
            p_r1, _ = UserProfile.objects.get_or_create(user=u_r1)
            p_r1.team = team_reignier
            p_r1.save()

            u_r2, _ = User.objects.get_or_create(
                username="agent2.reignier@demo.fr",
                defaults={
                    "email": "agent2.reignier@demo.fr",
                    "first_name": "Claire",
                    "last_name": "Lefevre",
                },
            )
            p_r2, _ = UserProfile.objects.get_or_create(user=u_r2)
            p_r2.team = team_reignier
            p_r2.save()

            # 2. Équipe Commune de Nangy
            team_nangy, _ = Team.objects.get_or_create(
                siret="21740198400013", defaults={"name": "Mairie de Nangy", "siren": "217401984"}
            )
            u_n1, _ = User.objects.get_or_create(
                username="agent1.nangy@demo.fr",
                defaults={
                    "email": "agent1.nangy@demo.fr",
                    "first_name": "Pierre",
                    "last_name": "Moreau",
                },
            )
            p_n1, _ = UserProfile.objects.get_or_create(user=u_n1)
            p_n1.team = team_nangy
            p_n1.save()

            # 3. Gendarmerie (Sans équipe)
            u_g1, _ = User.objects.get_or_create(
                username="gendarme1@demo.fr",
                defaults={
                    "email": "gendarme1@demo.fr",
                    "first_name": "Adjudant",
                    "last_name": "Bertrand",
                },
            )
            p_g1, _ = UserProfile.objects.get_or_create(user=u_g1)
            p_g1.team = None
            p_g1.save()

            u_g2, _ = User.objects.get_or_create(
                username="gendarme2@demo.fr",
                defaults={
                    "email": "gendarme2@demo.fr",
                    "first_name": "Maréchal",
                    "last_name": "Rousseau",
                },
            )
            p_g2, _ = UserProfile.objects.get_or_create(user=u_g2)
            p_g2.team = None
            p_g2.save()

            # 4. Dossiers Reignier (créés par agent1, modifiables par agent2)
            c_r1 = Constatation.objects.create(
                user=u_r1,
                created_by=u_r1,
                updated_by=u_r1,
                team=team_reignier,
                ceci_est_un_test=True,
                is_draft=False,
                commune="Reignier-Ésery",
                localisation_depot="Chemin de la Motte, près du ruisseau",
                date_constat=today - timedelta(days=5),
                auteur_identifie=True,
                statut_auteur="particulier",
                auteur_nom="Martin",
                auteur_prenom="Jean",
                precisions_depot="Gravats et cartons déposés de nuit",
            )
            sp_r1 = c_r1.suivi_procedure
            sp_r1.constatation_signee = True
            sp_r1.lettre_signe = True
            sp_r1.preuves_fournies = False
            sp_r1.updated_by = u_r1
            sp_r1.save()

            c_r2 = Constatation.objects.create(
                user=u_r1,
                created_by=u_r1,
                updated_by=u_r2,
                team=team_reignier,
                ceci_est_un_test=True,
                is_draft=False,
                commune="Reignier-Ésery",
                localisation_depot="Parking de l'école primaire",
                date_constat=today - timedelta(days=12),
                auteur_identifie=True,
                statut_auteur="particulier",
                auteur_nom="Bernard",
                auteur_prenom="Sophie",
                precisions_depot="Dépôt d'électroménager",
            )
            sp_r2 = c_r2.suivi_procedure
            for k, v in ENVOYE.items():
                setattr(sp_r2, k, v)
            sp_r2.lettre_envoyee_date = today - timedelta(days=10)
            sp_r2.ar_recu = True
            sp_r2.ar_statut = "distribue"
            sp_r2.ar_presentation_date = today - timedelta(days=8)
            sp_r2.updated_by = u_r2
            sp_r2.save()

            c_r3 = Constatation.objects.create(
                user=u_r2,
                created_by=u_r2,
                updated_by=u_r2,
                team=team_reignier,
                ceci_est_un_test=True,
                commune="Reignier-Ésery",
                localisation_depot="Chemin des Prés, près du point de tri",
                date_constat=today - timedelta(days=2),
                auteur_identifie=False,
                precisions_depot="Brouillon en cours d'enquête",
                is_draft=True,
            )

            # 5. Dossier Nangy
            c_n1 = Constatation.objects.create(
                user=u_n1,
                created_by=u_n1,
                updated_by=u_n1,
                team=team_nangy,
                ceci_est_un_test=True,
                commune="Nangy",
                localisation_depot="Route de Bonneville",
                date_constat=today - timedelta(days=7),
                auteur_identifie=True,
                statut_auteur="professionnel",
                auteur_nom="BTP Express",
                auteur_siret="38912345600018",
                precisions_depot="Pneus usagés",
            )
            sp_n1 = c_n1.suivi_procedure
            for k, v in {**ENVOYE, **SANCTION}.items():
                setattr(sp_n1, k, v)
            sp_n1.lettre_envoyee_date = today - timedelta(days=6)
            sp_n1.montant_amende = Decimal("1500")
            sp_n1.updated_by = u_n1
            sp_n1.save()

            # 6. Dossiers Gendarmerie
            c_g1 = Constatation.objects.create(
                user=u_g1,
                created_by=u_g1,
                updated_by=u_g1,
                team=None,
                ceci_est_un_test=True,
                commune="Chamonix-Mont-Blanc",
                localisation_depot="Sentier forestier",
                date_constat=today - timedelta(days=3),
                auteur_identifie=True,
                statut_auteur="particulier",
                auteur_nom="Faure",
                auteur_prenom="Lucas",
                precisions_depot="Bidons d'huile moteur",
            )
            sp_g1 = c_g1.suivi_procedure
            sp_g1.preuves_fournies = True
            sp_g1.constatation_signee = True
            sp_g1.updated_by = u_g1
            sp_g1.save()

            c_g2 = Constatation.objects.create(
                user=u_g2,
                created_by=u_g2,
                updated_by=u_g2,
                team=None,
                ceci_est_un_test=True,
                commune="Les Houches",
                localisation_depot="Route du Glacier",
                date_constat=today - timedelta(days=1),
                auteur_identifie=False,
                precisions_depot="Déchets verts et encombrants",
            )

        self.stdout.write(
            self.style.SUCCESS("Jeu de données de démo multi-équipes créé avec succès !")
        )
        self.stdout.write("Comptes créés pour /login-demo :")
        for email in demo_emails[:-1]:
            self.stdout.write(f"  - {email}")
