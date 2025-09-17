from django.core.management.base import BaseCommand

from backend.signalements.models import Signalement


class Command(BaseCommand):
    help = "Fix nature_terrain data before migration to JSONField"

    def handle(self, *args, **options):
        self.stdout.write("Fixing nature_terrain data...")
        for signalement in Signalement.objects.all():
            if not signalement.nature_terrain:
                # Empty values
                signalement.nature_terrain = "[]"
                signalement.save()
                self.stdout.write(f"Signalement {signalement.id}: empty -> []")
            elif isinstance(signalement.nature_terrain, list):
                # Already JSON - skip
                continue
            elif signalement.nature_terrain.startswith("[") and signalement.nature_terrain.endswith(
                "]"
            ):
                # JSON-like with single quotes
                old_value = signalement.nature_terrain
                signalement.nature_terrain = signalement.nature_terrain.replace("'", '"')
                signalement.save()
                self.stdout.write(
                    f"Signalement {signalement.id}: {old_value} -> {signalement.nature_terrain}"
                )
            else:
                # Plain strings - wrap in JSON array
                old_value = signalement.nature_terrain
                signalement.nature_terrain = f'["{signalement.nature_terrain}"]'
                signalement.save()
                self.stdout.write(
                    f"Signalement {signalement.id}: {old_value} -> {signalement.nature_terrain}"
                )
        self.stdout.write(self.style.SUCCESS("Data fix completed"))
