import logging

from django.core.management.base import BaseCommand

from backend.constatations.models import Constatation
from backend.dn_signalements.models import DNSignalement
from backend.procedures.models import SuiviProcedure

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Audit de l'intégrité de la structure et des relations de la base de données après migration."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING("\n=== DEBUT DE L'AUDIT DE L'INTEGRITE STRUCTURELLE DE LA DB ===")
        )

        # 1. Cohérence des volumes
        total_constatations = Constatation.objects.count()
        total_suivis = SuiviProcedure.objects.count()
        total_placeholders = DNSignalement.objects.count()

        self.stdout.write(f"➜ Constatations totales : {total_constatations}")
        self.stdout.write(f"➜ Suivis de procédures totaux : {total_suivis}")
        self.stdout.write(f"➜ DNSignalements (placeholders DN) : {total_placeholders}")

        # 2. Vérification des relations strictes (1-to-1)
        suivi_sans_constat = SuiviProcedure.objects.filter(constatation__isnull=True).count()
        suivi_sans_dn = SuiviProcedure.objects.filter(signalement__isnull=True).count()
        constat_sans_suivi = Constatation.objects.filter(suivi_procedure__isnull=True).count()

        self.stdout.write(self.style.WARNING("\n⚡ Anomalies de liaisons :"))
        self.stdout.write(
            f"  - Suivis sans Constatation : {suivi_sans_constat} (normal pour d'anciens signalements hors DN)"
        )
        self.stdout.write(f"  - Suivis sans DNSignalement (dossier DN) : {suivi_sans_dn}")
        self.stdout.write(f"  - Constatations sans Suivi : {constat_sans_suivi} (ATTENDU : 0)")

        errors_found = False
        if constat_sans_suivi > 0:
            self.stdout.write(
                self.style.ERROR(
                    "\n❌ ERREUR : Des constatations n'ont pas de suivi de procédure !"
                )
            )
            errors_found = True
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n✅ OK : Toutes les constatations possèdent un unique suivi de procédure."
                )
            )

        # 3. Vérification des dates historiques (idempotence temporelle)
        sample_constatations = Constatation.objects.filter(
            suivi_procedure__signalement__isnull=False
        )[:5]
        if sample_constatations.exists():
            self.stdout.write(
                self.style.WARNING(
                    "\n🕒 Échantillon des dates de création (historique DN préservé) :"
                )
            )
            for c in sample_constatations:
                dnsig = c.suivi_procedure.signalement
                self.stdout.write(
                    f"  - Dossier #{dnsig.dn_numero_dossier} | Commune : {c.commune} | Créé le : {c.created}"
                )

        self.stdout.write(self.style.WARNING("\n=== FIN DE L'AUDIT ==="))
        if errors_found:
            self.stdout.write(
                self.style.ERROR("L'audit a révélé des anomalies de liaisons de données.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Audit terminé avec succès. Aucune anomalie détectée.")
            )
