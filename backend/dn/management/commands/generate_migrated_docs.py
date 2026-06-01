import logging

from django.core.management.base import BaseCommand

from backend.constatations.models import Constatation

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Génère en arrière-plan les documents (rapport de constatation et lettre d'information) pour les dossiers DN migrés."

    def handle(self, *args, **options):
        self.stdout.write("Récupération de l'ensemble des constatations...")
        constatations = Constatation.objects.all()

        total_count = constatations.count()
        if total_count == 0:
            self.stdout.write(self.style.WARNING("Aucune constatation trouvée."))
            return

        self.stdout.write(self.style.WARNING(f"\nLancement de la génération des documents pour {total_count} constatation(s)..."))

        for idx, constatation in enumerate(constatations, start=1):
            dnsig = constatation.suivi_procedure.signalement if hasattr(constatation, "suivi_procedure") and constatation.suivi_procedure else None
            identifier = f"Dossier #{dnsig.dn_numero_dossier}" if dnsig else f"Constatation ID {constatation.id}"

            constatation.doc_constat_should_generate = True
            constatation.lettre_info_should_generate = True
            constatation.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"[{idx}/{total_count}] {identifier} : Demandes de génération envoyées (Rapport + Lettre)."
                )
            )

        self.stdout.write(self.style.SUCCESS("\n=================================================="))
        self.stdout.write(self.style.SUCCESS("    LANCEMENT DE LA GENERATION TERMINE AVEC SUCCES "))
        self.stdout.write(self.style.SUCCESS("=================================================="))
        self.stdout.write(f"Total des constatations traitées : {total_count}")
        self.stdout.write("Les documents (Rapports & Lettres) sont générés en arrière-plan par les tâches de fond.\n")
