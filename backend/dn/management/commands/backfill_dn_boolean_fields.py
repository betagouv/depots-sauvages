import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from backend.constatations.models import Constatation
from backend.dn.client import DNGraphQLClient
from backend.dn_signalements.models import DNSignalement
from backend.dn_signalements.views import ProcessDossierView
from backend.procedures.models import SuiviProcedure

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Backfill missing DN boolean fields (entreprise_francaise and ceci_est_un_test) from DN API without overwriting user-modified data."

    def handle(self, *args, **options):
        self.stdout.write(
            "Début du rattrapage des champs booléens depuis l'API Démarches Numériques..."
        )

        try:
            dn_client = DNGraphQLClient()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Impossible d'initialiser le client DN API : {e}"))
            return

        parser_view = ProcessDossierView()

        # Fetch all local DNSignalements
        dnsigs = DNSignalement.objects.all().order_by("dn_numero_dossier")
        total_placeholders = dnsigs.count()

        if total_placeholders == 0:
            self.stdout.write(self.style.WARNING("Aucun signalement DN trouvé en base locale."))
            return

        self.stdout.write(f"Analyse de {total_placeholders} signalements DN...")

        stats = {
            "total": total_placeholders,
            "no_constatation": 0,
            "skipped_already_filled": 0,
            "updated_constatations": 0,
            "updated_entreprise_francaise": 0,
            "updated_ceci_est_un_test": 0,
            "errors": 0,
        }

        updated_details = []

        for idx, dnsig in enumerate(dnsigs, start=1):
            dossier_number = dnsig.dn_numero_dossier
            sp = SuiviProcedure.objects.filter(signalement=dnsig).first()
            constatation = sp.constatation if sp else None

            if not constatation:
                stats["no_constatation"] += 1
                continue

            # Check if both fields are already filled in the constatation (we do not overwrite)
            ent_filled = constatation.entreprise_francaise is not None
            test_filled = constatation.ceci_est_un_test is not None

            if ent_filled and test_filled:
                stats["skipped_already_filled"] += 1
                continue

            self.stdout.write(
                f"[{idx}/{total_placeholders}] Récupération des détails pour le dossier #{dossier_number}..."
            )

            try:
                dossier_detail = dn_client.get_dossier(dossier_number)
                if not dossier_detail:
                    self.stdout.write(
                        self.style.WARNING(f"  Dossier #{dossier_number} non trouvé sur l'API.")
                    )
                    stats["errors"] += 1
                    continue

                signalement_data = parser_view.dossier_to_model_data(dossier_detail)
                if not signalement_data:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  Impossible d'extraire les données pour le dossier #{dossier_number}."
                        )
                    )
                    stats["errors"] += 1
                    continue

                api_entreprise_francaise = signalement_data.get("entreprise_francaise")
                api_ceci_est_un_test = signalement_data.get("ceci_est_un_test")

                updated_fields = []
                with transaction.atomic():
                    # Refresh from DB to lock the row and avoid race conditions
                    constatation = Constatation.objects.select_for_update().get(id=constatation.id)
                    dnsig = DNSignalement.objects.select_for_update().get(id=dnsig.id)

                    save_constat = False
                    save_dnsig = False

                    # Backfill entreprise_francaise
                    if (
                        constatation.entreprise_francaise is None
                        and api_entreprise_francaise is not None
                    ):
                        constatation.entreprise_francaise = api_entreprise_francaise
                        save_constat = True
                        stats["updated_entreprise_francaise"] += 1
                        updated_fields.append(f"entreprise_francaise={api_entreprise_francaise}")

                    if dnsig.entreprise_francaise is None and api_entreprise_francaise is not None:
                        dnsig.entreprise_francaise = api_entreprise_francaise
                        save_dnsig = True

                    # Backfill ceci_est_un_test
                    if constatation.ceci_est_un_test is None and api_ceci_est_un_test is not None:
                        constatation.ceci_est_un_test = api_ceci_est_un_test
                        save_constat = True
                        stats["updated_ceci_est_un_test"] += 1
                        updated_fields.append(f"ceci_est_un_test={api_ceci_est_un_test}")

                    if dnsig.ceci_est_un_test is None and api_ceci_est_un_test is not None:
                        dnsig.ceci_est_un_test = api_ceci_est_un_test
                        save_dnsig = True

                    if save_constat:
                        constatation.save()
                        stats["updated_constatations"] += 1

                    if save_dnsig:
                        dnsig.save()

                if updated_fields:
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✓ Mis à jour : {', '.join(updated_fields)}")
                    )
                    updated_details.append(
                        {
                            "dossier": dossier_number,
                            "commune": constatation.commune,
                            "updates": ", ".join(updated_fields),
                        }
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"  Erreur lors de la mise à jour pour le dossier #{dossier_number} : {e}"
                    )
                )
                stats["errors"] += 1

        # --- RAPPORT ---
        self.stdout.write(
            self.style.SUCCESS("\n==================================================")
        )
        self.stdout.write(self.style.SUCCESS("    RAPPORT DE RATTRAPAGE DES CHAMPS BOOLÉENS DN   "))
        self.stdout.write(self.style.SUCCESS("=================================================="))
        self.stdout.write(f"Nombre total de dossiers analysés           : {stats['total']}")
        self.stdout.write(
            f"Ignorés (champs déjà remplis par l'usager)  : {stats['skipped_already_filled']}"
        )
        self.stdout.write(
            f"Ignorés (pas de constatation liée en base)  : {stats['no_constatation']}"
        )
        self.stdout.write(f"Dossiers avec erreurs de traitement         : {stats['errors']}")
        self.stdout.write(self.style.SUCCESS("--------------------------------------------------"))
        self.stdout.write(
            self.style.SUCCESS(
                f"Constatations mises à jour avec succès      : {stats['updated_constatations']}"
            )
        )
        self.stdout.write(
            f"  - Rattrapages 'entreprise_francaise'      : {stats['updated_entreprise_francaise']}"
        )
        self.stdout.write(
            f"  - Rattrapages 'ceci_est_un_test'          : {stats['updated_ceci_est_un_test']}"
        )
        self.stdout.write(
            self.style.SUCCESS("==================================================\n")
        )

        if updated_details:
            self.stdout.write(self.style.SUCCESS("DÉTAIL DES MISES À JOUR EFFECTUÉES :"))
            self.stdout.write("-" * 80)
            self.stdout.write(
                f"{'Dossier DN':<15} | {'Commune':<25} | {'Mises à jour effectuées':<35}"
            )
            self.stdout.write("-" * 80)
            for item in updated_details:
                self.stdout.write(
                    f"#{item['dossier']:<14} | {item['commune']:<25} | {item['updates']:<35}"
                )
            self.stdout.write("-" * 80)
            self.stdout.write("\n")
