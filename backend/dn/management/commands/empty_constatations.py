import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from backend.constatations.models import Constatation
from backend.procedures.models import SuiviProcedure

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Clear all Constatation records and unlink SuiviProcedures."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING("--- Commencing local cleanup (empty constatations) ---")
        )
        with transaction.atomic():
            # Unlink SuiviProcedure from constatations
            sp_updated = SuiviProcedure.objects.filter(constatation__isnull=False).update(
                constatation=None
            )
            self.stdout.write(
                f"Unlinked {sp_updated} SuiviProcedure records from Constatations."
            )

            # Delete all existing constatations
            deleted_count, _ = Constatation.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully deleted {deleted_count} local Constatation records."
                )
            )
