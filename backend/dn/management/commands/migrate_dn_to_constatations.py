import logging
import re

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import dateparse, timezone

from backend.constatations.models import Constatation
from backend.dn.client import DNGraphQLClient
from backend.dn.queries import GET_DEMARCHE_DOSSIERS_LEAN_QUERY
from backend.dn_signalements.models import DNSignalement
from backend.dn_signalements.views import ProcessDossierView
from backend.procedures.models import SuiviProcedure

logger = logging.getLogger(__name__)
User = get_user_model()


class Command(BaseCommand):
    help = "Migrate dossiers directly from the Démarche Numériques API into local Constatations."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-pre-register",
            action="store_true",
            help="Disable default pre-registration of unmatched user accounts.",
        )
        parser.add_argument(
            "--no-update",
            action="store_true",
            help="Skip updating already migrated/existing constatations (create-only mode).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simulate the migration without modifying the database and show which dossiers would be processed.",
        )

    def handle(self, *args, **options):
        no_pre_register = options["no_pre_register"]
        no_update = options.get("no_update")
        dry_run = options.get("dry_run")

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

        if no_update:
            existing_dossiers = set(
                SuiviProcedure.objects.filter(
                    signalement__dn_numero_dossier__isnull=False,
                    constatation__isnull=False
                ).values_list("signalement__dn_numero_dossier", flat=True)
            )
            lean_dossiers = [
                node for node in lean_dossiers
                if node.get("number") not in existing_dossiers
            ]

        total_source_count = len(lean_dossiers)
        if total_source_count == 0:
            self.stdout.write(self.style.WARNING("Aucun dossier trouvé sur l'API DN avec ces critères."))
            return

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"\n[DRY RUN] {total_source_count} dossiers seraient importés ou mis à jour :"
                )
            )
            self.stdout.write("-" * 65)
            self.stdout.write(f"{'Dossier DN':<15} | {'Date de dépôt (DN)':<30} | {'Email':<25}")
            self.stdout.write("-" * 65)
            for node in lean_dossiers:
                email = node.get("usager", {}).get("email") or "[Non renseigné]"
                self.stdout.write(
                    f"{node.get('number'):<15} | {node.get('dateDepot') or '[Inconnue]':<30} | {email:<25}"
                )
            self.stdout.write("-" * 65)
            self.stdout.write(
                self.style.WARNING(
                    "[DRY RUN] Fin de la simulation. Aucune modification n'a été effectuée en base de données.\n"
                )
            )
            return

        self.stdout.write(
            f"{total_source_count} dossiers trouvés sur l'API DN. Début de l'importation..."
        )
        migrated_count = 0
        fallbacks_applied = []
        procedures_relinked = 0
        procedures_created = 0
        unmatched_users_logged = []
        pre_registered_users = []
        # Instantiate ProcessDossierView to reuse parsing and extraction logic
        parser_view = ProcessDossierView()

        # Temporarily disconnect post_save signals on Constatation to avoid automatic/conflicting
        # SuiviProcedure creation and background document task queueing during the migration.
        from django.db.models.signals import post_save

        from backend.signalements.signals import (
            create_suivi_procedure,
            generate_doc_constat,
            generate_lettre_info,
        )

        post_save.disconnect(create_suivi_procedure, sender=Constatation)
        post_save.disconnect(generate_doc_constat, sender=Constatation)
        post_save.disconnect(generate_lettre_info, sender=Constatation)

        try:
            for idx, lean_node in enumerate(lean_dossiers, start=1):
                dossier_number = lean_node["number"]
                self.stdout.write(
                    f"[{idx}/{total_source_count}] Récupération des détails complets pour le dossier #{dossier_number}..."
                )
                try:
                    dossier_detail = dn_client.get_dossier(dossier_number)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"  Erreur lors de la récupération des détails pour le dossier #{dossier_number} : {e}"
                        )
                    )
                    continue

                if not dossier_detail:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  Le dossier #{dossier_number} n'a pas été trouvé sur l'API."
                        )
                    )
                    continue
                # Extract model data
                signalement_data = parser_view.dossier_to_model_data(dossier_detail, ignore_missing_date=True)
                if not signalement_data:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  Le dossier #{dossier_number} n'a pas de procédure associée ou manque d'informations, ignoré."
                        )
                    )
                    continue
                # Clean signalement_data to only include fields existing on the Constatation model
                valid_fields = {field.name for field in Constatation._meta.get_fields()}
                signalement_data = {k: v for k, v in signalement_data.items() if k in valid_fields}
                # Map or pre-register the associated user
                user = None
                usager_email = dossier_detail.get("usager", {}).get("email")
                if usager_email:
                    user = User.objects.filter(email__iexact=usager_email).first()
                    if not user:
                        user = User.objects.filter(username__iexact=usager_email).first()
                    if not user:
                        if no_pre_register:
                            unmatched_users_logged.append(
                                {
                                    "dossier": dossier_number,
                                    "email": usager_email,
                                }
                            )
                        else:
                            # Pre-register user cleanly (fully idempotent check done above)
                            user = User.objects.create(
                                email=usager_email,
                                username=usager_email,
                                is_active=True,
                            )
                            pre_registered_users.append(
                                {
                                    "dossier": dossier_number,
                                    "email": usager_email,
                                }
                            )
                # Handle Commune Fallback
                commune = signalement_data.get("commune")
                if not commune or not commune.strip():
                    # Heuristics parsing: check if we can extract commune from localisation_depot
                    parsed_commune = None
                    loc = signalement_data.get("localisation_depot") or ""
                    if loc:
                        match = re.search(r"\b\d{5}\s+([A-Za-zÀ-ÖØ-öø-ÿ\s\-]+)$", loc)
                        if match:
                            parsed_commune = match.group(1).strip()
                    commune = parsed_commune or "Inconnue"
                    fallbacks_applied.append(
                        {
                            "dossier": dossier_number,
                            "localisation": loc or "[Vide]",
                            "assigned": commune,
                        }
                    )
                    signalement_data["commune"] = commune
                # Normalize role présidents de l'epci if needed
                role = signalement_data.get("constatant_role") or ""
                if "président de l'epci" in role.lower() or "président de l’epci" in role.lower():
                    signalement_data["constatant_role"] = "president ECPI"
                # Parse original timestamps
                date_creation = (
                    dateparse.parse_datetime(dossier_detail.get("dateDepot")) or timezone.now()
                )
                date_modification = (
                    dateparse.parse_datetime(dossier_detail.get("dateDerniereModification"))
                    or timezone.now()
                )
                # Doc generation will be done later, when the user hits the "suivi procédure" page.
                signalement_data["doc_constat_should_generate"] = False
                signalement_data["lettre_info_should_generate"] = False
                with transaction.atomic():
                    # Get or create the DNSignalement placeholder to ensure robust tracking & idempotency
                    dnsig, _ = DNSignalement.objects.get_or_create(
                        dn_numero_dossier=dossier_number,
                        defaults={
                            "commune": commune,
                            "localisation_depot": signalement_data.get("localisation_depot") or "",
                            "date_constat": signalement_data.get("date_constat"),
                            "heure_constat": signalement_data.get("heure_constat"),
                        },
                    )
                    # Locate corresponding SuiviProcedure linked to this dossier's placeholder
                    sp = SuiviProcedure.objects.filter(signalement=dnsig).first()
                    constatation = None
                    if sp and sp.constatation:
                        constatation = sp.constatation
                    is_new_constatation = False
                    if constatation:
                        # Update existing constatation (IDEMPOTENT update)
                        for k, v in signalement_data.items():
                            setattr(constatation, k, v)
                        constatation.user = user
                        constatation.save()
                    else:
                        # Create new constatation (no signal will trigger to auto-create SuiviProcedure)
                        constatation = Constatation.objects.create(user=user, **signalement_data)
                        is_new_constatation = True
                    # Overwrite django's auto-generated created/modified times with original ones
                    Constatation.objects.filter(id=constatation.id).update(
                        created=date_creation, modified=date_modification
                    )
                    # Connect SuiviProcedure safely
                    if sp:
                        # If there's an existing SuiviProcedure for this dossier, link it to the constatation
                        if sp.constatation != constatation:
                            sp.constatation = constatation
                            sp.save()
                        procedures_relinked += 1
                    else:
                        # Create new SuiviProcedure safely since signal didn't create one
                        sp = SuiviProcedure.objects.create(
                            constatation=constatation, signalement=dnsig
                        )
                        procedures_created += 1
                    migrated_count += 1
        finally:
            post_save.connect(create_suivi_procedure, sender=Constatation)
            post_save.connect(generate_doc_constat, sender=Constatation)
            post_save.connect(generate_lettre_info, sender=Constatation)

        # --- MIGRATION REPORT ---
        self.stdout.write(
            self.style.SUCCESS("\n==================================================")
        )
        self.stdout.write(
            self.style.SUCCESS("    MIGRATION DES DONNÉES DE L'API TERMINÉE AVEC SUCCÈS   ")
        )
        self.stdout.write(self.style.SUCCESS("=================================================="))
        self.stdout.write(f"Nombre total de Constatations créées/mises à jour : {migrated_count}")
        self.stdout.write(f"Nombre total de SuiviProcedure réassociés : {procedures_relinked}")
        self.stdout.write(f"Nombre total de SuiviProcedure créés : {procedures_created}")
        self.stdout.write("==================================================\n")

        # Warning list of unmatched users (when pre-registration is disabled)
        if unmatched_users_logged:
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️  DOSSIERS IMPORTÉS SANS UTILISATEUR DJANGO LOCAL (aucun utilisateur assigné) :"
                )
            )
            self.stdout.write("-" * 80)
            self.stdout.write(f"{'Dossier DN':<15} | {'Usager Email (DN)':<45}")
            self.stdout.write("-" * 80)
            for item in unmatched_users_logged:
                self.stdout.write(f"{item['dossier']:<15} | {item['email']:<45}")
            self.stdout.write("-" * 80)
            self.stdout.write(
                f"Total des dossiers sans utilisateur Django : {len(unmatched_users_logged)}"
            )
            self.stdout.write("Note : La pré-inscription a été ignorée (--no-pre-register).\n")

        # Dynamic Pre-Registration Report
        if pre_registered_users:
            self.stdout.write(
                self.style.SUCCESS(f"✓ COMPTES UTILISATEURS DJANGO CRÉÉS DYNAMIQUEMENT :")
            )
            self.stdout.write("-" * 80)
            self.stdout.write(f"{'Dossier DN':<15} | {'Email du compte créé (DN)':<45}")
            self.stdout.write("-" * 80)
            for item in pre_registered_users:
                self.stdout.write(f"{item['dossier']:<15} | {item['email']:<45}")
            self.stdout.write("-" * 80)
            self.stdout.write(
                f"Total des comptes créés dynamiquement : {len(pre_registered_users)}\n"
            )

        if fallbacks_applied:
            self.stdout.write(
                self.style.WARNING(
                    "⚠️  DOSSIERS AVEC COMMUNE PAR DÉFAUT GÉNÉRÉE (Vérification manuelle recommandée) :"
                )
            )
            self.stdout.write("-" * 80)
            self.stdout.write(
                f"{'Dossier DN':<15} | {'Commune assignée':<25} | {'Adresse de localisation':<35}"
            )
            self.stdout.write("-" * 80)
            for item in fallbacks_applied:
                loc_short = (
                    item["localisation"][:33] + "..."
                    if len(item["localisation"]) > 33
                    else item["localisation"]
                )
                loc_short = loc_short.replace("\n", " ").replace("\r", " ")
                self.stdout.write(
                    f"{item['dossier']:<15} | {item['assigned']:<25} | {loc_short:<35}"
                )
            self.stdout.write("-" * 80)
            self.stdout.write(
                f"Total des dossiers nécessitant une vérification manuelle : {len(fallbacks_applied)}"
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "✓ Tous les dossiers avaient des valeurs de commune valides. Aucune valeur par défaut n'a été nécessaire."
                )
            )

        self.stdout.write("\n")
