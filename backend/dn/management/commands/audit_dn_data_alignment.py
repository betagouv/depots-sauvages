import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import dateparse

from backend.constatations.models import Constatation
from backend.dn.client import DNGraphQLClient
from backend.dn.queries import GET_DEMARCHE_DOSSIERS_LEAN_QUERY
from backend.dn_signalements.models import DNSignalement
from backend.dn_signalements.views import ProcessDossierView

logger = logging.getLogger(__name__)
User = get_user_model()


class Command(BaseCommand):
    help = "Audit d'alignement détaillé des champs de données entre l'API Démarches Numériques et la base locale."

    def handle(self, *args, **options):
        self.stdout.write(
            "Récupération de la liste des dossiers depuis l'API Démarches Numériques..."
        )
        try:
            dn_client = DNGraphQLClient()
            lean_dossiers = dn_client.get_dossiers_for_demarche(
                query=GET_DEMARCHE_DOSSIERS_LEAN_QUERY
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Échec de la récupération de la liste des dossiers depuis l'API DN : {e}"
                )
            )
            return

        total_source_count = len(lean_dossiers)
        if total_source_count == 0:
            self.stdout.write(self.style.WARNING("Aucun dossier trouvé sur l'API DN."))
            return

        self.stdout.write(
            self.style.WARNING(
                f"\n=== DEBUT DE L'AUDIT D'ALIGNEMENT DETAILLE DES CHAMPS ({total_source_count} dossiers) ==="
            )
        )

        parser_view = ProcessDossierView()
        valid_fields = {field.name for field in Constatation._meta.get_fields()}

        alignment_discrepancies = []
        fully_aligned_count = 0
        missing_in_db_count = 0

        for idx, lean_node in enumerate(lean_dossiers, start=1):
            dossier_number = lean_node["number"]
            self.stdout.write(
                f"[{idx}/{total_source_count}] Analyse du dossier #{dossier_number}..."
            )

            # 1. Check if placeholders exist in DB
            dnsig = DNSignalement.objects.filter(dn_numero_dossier=dossier_number).first()
            if not dnsig:
                missing_in_db_count += 1
                alignment_discrepancies.append(
                    {
                        "dossier": dossier_number,
                        "field": "DNSignalement",
                        "api_val": "Présent",
                        "db_val": "Absent en base locale",
                    }
                )
                continue

            # Locate corresponding Constatation
            sp = dnsig.suivi_procedure if hasattr(dnsig, "suivi_procedure") else None
            constatation = sp.constatation if sp else None
            if not constatation:
                missing_in_db_count += 1
                alignment_discrepancies.append(
                    {
                        "dossier": dossier_number,
                        "field": "Constatation / Suivi",
                        "api_val": "Présent",
                        "db_val": "Aucune Constatation liée",
                    }
                )
                continue

            # Fetch full details from DN API to compare fields
            try:
                dossier_detail = dn_client.get_dossier(dossier_number)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"  Erreur lors de la récupération pour #{dossier_number} : {e}"
                    )
                )
                continue

            if not dossier_detail:
                continue

            # Extract expected model data
            expected_data = parser_view.dossier_to_model_data(dossier_detail, ignore_missing_date=True)
            if not expected_data:
                continue
            expected_data = {k: v for k, v in expected_data.items() if k in valid_fields}

            dossier_discrepancies = []

            # Compare Constatation fields
            for field_name, expected_val in expected_data.items():
                # Skip commune check here if we want to handle commune fallback
                if field_name == "commune" and not expected_val:
                    continue  # Fallback was applied, so it won't match empty val

                db_val = getattr(constatation, field_name, None)

                # Normalize values for fair comparison (strip, convert None to empty, etc.)
                norm_expected = (
                    (expected_val or "").strip() if isinstance(expected_val, str) else expected_val
                )
                norm_db = (db_val or "").strip() if isinstance(db_val, str) else db_val

                # Normalize dates to compare only the date part YYYY-MM-DD
                if field_name == "date_constat":
                    import datetime

                    if isinstance(expected_val, (datetime.datetime, datetime.date)):
                        norm_expected = (
                            expected_val.date()
                            if isinstance(expected_val, datetime.datetime)
                            else expected_val
                        )
                    elif isinstance(expected_val, str) and expected_val.strip():
                        parsed = dateparse.parse_datetime(expected_val) or dateparse.parse_date(
                            expected_val
                        )
                        if parsed:
                            norm_expected = (
                                parsed.date() if isinstance(parsed, datetime.datetime) else parsed
                            )

                    if isinstance(db_val, (datetime.datetime, datetime.date)):
                        norm_db = db_val.date() if isinstance(db_val, datetime.datetime) else db_val
                    elif isinstance(db_val, str) and db_val.strip():
                        parsed = dateparse.parse_datetime(db_val) or dateparse.parse_date(db_val)
                        if parsed:
                            norm_db = (
                                parsed.date() if isinstance(parsed, datetime.datetime) else parsed
                            )

                if norm_expected != norm_db:
                    # Role normalization check
                    if (
                        field_name == "constatant_role"
                        and norm_db == "president ECPI"
                        and norm_expected
                        and ("président de l" in norm_expected.lower())
                    ):
                        continue

                    dossier_discrepancies.append(
                        {
                            "dossier": dossier_number,
                            "field": f"Constatation.{field_name}",
                            "api_val": str(norm_expected)[:40],
                            "db_val": str(norm_db)[:40],
                        }
                    )

            # Compare associated User
            usager_email = dossier_detail.get("usager", {}).get("email")
            db_user_email = constatation.user.email if constatation.user else None
            if usager_email and db_user_email and usager_email.lower() != db_user_email.lower():
                dossier_discrepancies.append(
                    {
                        "dossier": dossier_number,
                        "field": "User.email",
                        "api_val": usager_email,
                        "db_val": db_user_email,
                    }
                )

            # Compare Timestamps
            date_creation = dateparse.parse_datetime(dossier_detail.get("dateDepot"))
            if date_creation and constatation.created.date() != date_creation.date():
                dossier_discrepancies.append(
                    {
                        "dossier": dossier_number,
                        "field": "Constatation.created (Date)",
                        "api_val": date_creation.date().isoformat(),
                        "db_val": constatation.created.date().isoformat(),
                    }
                )

            if dossier_discrepancies:
                alignment_discrepancies.extend(dossier_discrepancies)
            else:
                fully_aligned_count += 1

        # --- AUDIT REPORT ---
        self.stdout.write(self.style.WARNING("\n=== RAPPORT D'ALIGNEMENT DETAILLE DES DONNÉES ==="))
        self.stdout.write(
            f"Dossiers totalement alignés : {fully_aligned_count}/{total_source_count}"
        )
        self.stdout.write(f"Dossiers absents/incomplets en base : {missing_in_db_count}")

        if alignment_discrepancies:
            self.stdout.write(
                self.style.WARNING(
                    f"\n⚠️  {len(alignment_discrepancies)} Écarts d'alignement détectés entre l'API DN et la DB locale :"
                )
            )
            self.stdout.write("-" * 120)
            self.stdout.write(
                f"{'Dossier':<10} | {'Champ concerné':<30} | {'Valeur attendue (API DN)':<35} | {'Valeur réelle (Base de données)':<35}"
            )
            self.stdout.write("-" * 120)
            for item in alignment_discrepancies:
                self.stdout.write(
                    f"#{item['dossier']:<9} | {item['field']:<30} | {item['api_val']:<35} | {item['db_val']:<35}"
                )
            self.stdout.write("-" * 120)
            self.stdout.write(
                self.style.ERROR(
                    "Audit d'alignement terminé : des différences de données ou des dossiers manquants ont été repérés."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n✓ Alignement parfait ! Toutes les données en base correspondent exactement aux valeurs de l'API DN."
                )
            )
        self.stdout.write("\n")
