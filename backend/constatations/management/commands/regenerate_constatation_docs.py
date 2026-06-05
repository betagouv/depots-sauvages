import logging

from django.core.management.base import BaseCommand

from backend.constatations.models import Constatation

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Force la régénération des documents (rapport de constatation et lettre d'information) des constatations."

    def add_arguments(self, parser):
        parser.add_argument(
            "--only-constat",
            action="store_true",
            help="Régénérer uniquement les rapports de constatation.",
        )
        parser.add_argument(
            "--only-lettre",
            action="store_true",
            help="Régénérer uniquement les lettres d'information (seulement si l'auteur est identifié).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simule l'opération sans sauvegarder ni lancer la génération.",
        )

    def handle(self, *args, **options):
        only_constat = options["only_constat"]
        only_lettre = options["only_lettre"]
        dry_run = options["dry_run"]
        # If neither is specified, regenerate both
        regenerate_constat = not only_lettre
        regenerate_lettre = not only_constat
        self.stdout.write("Récupération de l'ensemble des constatations...")
        constatations = Constatation.objects.all()
        total_count = constatations.count()
        if total_count == 0:
            self.stdout.write(self.style.WARNING("Aucune constatation trouvée."))
            return
        self.stdout.write(
            self.style.WARNING(
                f"\nTraitement de {total_count} constatation(s)... (dry-run={dry_run})"
            )
        )
        success_count = 0
        for constatation in constatations:
            identifier = f"Constatation ID {constatation.id}"
            to_save = False
            actions = []
            if regenerate_constat:
                constatation.doc_constat_should_generate = True
                to_save = True
                actions.append("Rapport")
            if regenerate_lettre:
                if constatation.auteur_identifie:
                    constatation.lettre_info_should_generate = True
                    to_save = True
                    actions.append("Lettre")
                else:
                    self.stdout.write(
                        self.style.WARNING(f"{identifier} : Lettre ignorée (auteur non identifié).")
                    )
            if to_save:
                if not dry_run:
                    constatation.save()
                success_count += 1
                action_str = " + ".join(actions)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{identifier} : Demande de génération ({action_str}) enregistrée."
                    )
                )
        self.stdout.write(
            self.style.SUCCESS("\n==================================================")
        )
        if dry_run:
            self.stdout.write(self.style.SUCCESS("    SIMULATION (DRY-RUN) TERMINEE AVEC SUCCES "))
        else:
            self.stdout.write(
                self.style.SUCCESS("    LANCEMENT DE LA GENERATION TERMINE AVEC SUCCES ")
            )
        self.stdout.write(self.style.SUCCESS("=================================================="))
        self.stdout.write(f"Total des constatations traitées : {total_count}")
        self.stdout.write(f"Total des constatations modifiées : {success_count}")
        if not dry_run:
            self.stdout.write(
                "Les documents demandés sont générés en arrière-plan par les tâches de fond.\n"
            )
