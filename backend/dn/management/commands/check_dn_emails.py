import logging
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from backend.dn.client import DNGraphQLClient
from backend.dn.queries import GET_DEMARCHE_DOSSIERS_LEAN_QUERY

logger = logging.getLogger(__name__)
User = get_user_model()


class Command(BaseCommand):
    help = "Audit à blanc : compare les e-mails des usagers de l'API DN avec les utilisateurs locaux Django et affiche les enregistrements non correspondants."

    def handle(self, *args, **options):
        self.stdout.write("Récupération de la liste des dossiers depuis l'API Démarches Numériques...")
        try:
            dn_client = DNGraphQLClient()
            lean_dossiers = dn_client.get_dossiers_for_demarche(
                query=GET_DEMARCHE_DOSSIERS_LEAN_QUERY
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Échec de la récupération de la liste des dossiers depuis l'API DN : {e}"))
            return

        total_source_count = len(lean_dossiers)
        if total_source_count == 0:
            self.stdout.write(self.style.WARNING("Aucun dossier trouvé sur l'API DN."))
            return

        self.stdout.write(self.style.WARNING("\n=== Mode de vérification des e-mails : API DN vs Utilisateurs Django ==="))
        self.stdout.write(f"Audit de {total_source_count} dossiers par rapport à la base de données locale des utilisateurs...\n")

        unmatched_records = []
        matched_count = 0

        for node in lean_dossiers:
            dossier_number = node["number"]
            email = node.get("usager", {}).get("email")

            if not email:
                unmatched_records.append({
                    "dossier": dossier_number,
                    "email": "[Aucun e-mail renseigné]",
                    "reason": "Adresse e-mail manquante sur le dossier DN",
                })
                continue

            user_exists = User.objects.filter(email__iexact=email).exists() or User.objects.filter(username__iexact=email).exists()
            if user_exists:
                matched_count += 1
            else:
                unmatched_records.append({
                    "dossier": dossier_number,
                    "email": email,
                    "reason": "Aucun utilisateur Django ne correspond à cet e-mail",
                })

        self.stdout.write(self.style.SUCCESS(f"Utilisateurs correspondants trouvés dans Django : {matched_count}/{total_source_count}"))
        
        if unmatched_records:
            self.stdout.write(self.style.WARNING(f"\n⚠️  Trouvé {len(unmatched_records)} dossiers sans correspondance (aucun utilisateur Django correspondant) :"))
            self.stdout.write("-" * 80)
            self.stdout.write(f"{'Dossier DN':<15} | {'Adresse e-mail de l’usager':<35} | {'Problème/Raison':<30}")
            self.stdout.write("-" * 80)
            for item in unmatched_records:
                self.stdout.write(f"{item['dossier']:<15} | {item['email']:<35} | {item['reason']:<30}")
            self.stdout.write("-" * 80)
        else:
            self.stdout.write(self.style.SUCCESS("✓ Correspondance parfaite ! Tous les dossiers DN ont un utilisateur local Django correspondant."))
        self.stdout.write("\n")
