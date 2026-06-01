import logging
from django.core.management.base import BaseCommand
from backend.constatations.models import Constatation

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Génère en arrière-plan les documents (rapport de constatation et lettre d'information) pour les dossiers DN migrés."

    def handle(self, *args, **options):
        self.stdout.write("Recherche des constatations migrées nécessitant la génération de documents...")

        # Find Constatations that have a linked DNSignalement (migrated dossiers)
        migrated_constatations = Constatation.objects.filter(
            suivi_procedure__signalement__isnull=False
        )

        total_count = migrated_constatations.count()
        if total_count == 0:
            self.stdout.write(self.style.WARNING("Aucune constatation migrée trouvée."))
            return

        self.stdout.write(f"Trouvé {total_count} constatation(s) migrée(s). Début de l'analyse...")

        doc_constat_triggered = 0
        lettre_info_triggered = 0

        for idx, constatation in enumerate(migrated_constatations, start=1):
            dossier_num = constatation.suivi_procedure.signalement.dn_numero_dossier
            needs_save = False
            triggered_actions = []

            # 1. Trigger Rapport de constatation if not yet generated
            if not constatation.doc_constat:
                constatation.doc_constat_should_generate = True
                needs_save = True
                doc_constat_triggered += 1
                triggered_actions.append("Rapport de constatation")

            # 2. Trigger Lettre d'information if auteur is identified and not yet generated
            # Note: doc generation signal checks lettre_info_should_generate
            if constatation.auteur_identifie and not constatation.lettre_info:
                constatation.lettre_info_should_generate = True
                needs_save = True
                lettre_info_triggered += 1
                triggered_actions.append("Lettre d'information")

            if needs_save:
                # Saving with signals active automatically enqueues background document generation tasks
                constatation.save()
                actions_str = " et ".join(triggered_actions)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"[{idx}/{total_count}] Dossier #{dossier_num} : Génération lancée pour : {actions_str}."
                    )
                )
            else:
                self.stdout.write(
                    f"[{idx}/{total_count}] Dossier #{dossier_num} : Documents déjà générés ou non requis, ignoré."
                )

        self.stdout.write(self.style.SUCCESS("\n=================================================="))
        self.stdout.write(self.style.SUCCESS("    LANCEMENT DE LA GENERATION TERMINE AVEC SUCCES "))
        self.stdout.write(self.style.SUCCESS("=================================================="))
        self.stdout.write(f"Rapports de constatation en cours de génération : {doc_constat_triggered}")
        self.stdout.write(f"Lettres d'information en cours de génération    : {lettre_info_triggered}")
        self.stdout.write("Les documents sont générés de manière asynchrone par les tâches de fond.\n")
