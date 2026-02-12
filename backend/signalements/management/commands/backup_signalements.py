import csv
import os
import sys
from datetime import datetime

from django.core.management.base import BaseCommand

from backend.signalements.models import Signalement


class Command(BaseCommand):
    help = "Backup old Signalement data to CSV."

    def add_arguments(self, parser):
        parser.add_argument(
            "--stdout", action="store_true", help="Output to stdout instead of file"
        )
        parser.add_argument("--output", type=str, help="Output file name")

    def handle(self, *args, **options):
        to_stdout = options["stdout"]
        output_file = options["output"]
        # Get all fields from the model
        fields = [field.name for field in Signalement._meta.fields]
        queryset = Signalement.objects.all()
        if not queryset.exists():
            if not to_stdout:
                self.stdout.write(self.style.WARNING("No data found in 'Signalement' table."))
            return
        if not to_stdout:
            self.stdout.write(
                self.style.SUCCESS(f"Model found. Starting export of {queryset.count()} records...")
            )
        if to_stdout:
            writer = csv.writer(sys.stdout)
            writer.writerow(fields)
            for obj in queryset:
                row = [getattr(obj, field) for field in fields]
                writer.writerow(row)
        else:
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"backup_signalements_orm_{timestamp}.csv"
            with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(fields)
                for obj in queryset:
                    row = [getattr(obj, field) for field in fields]
                    writer.writerow(row)
            self.stdout.write(self.style.SUCCESS("Backup completed successfully!"))
            self.stdout.write(f"File created: {os.path.abspath(output_file)}")
            self.stdout.write(f"Row count: {queryset.count()}")
