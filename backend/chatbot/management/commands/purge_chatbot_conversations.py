from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from backend.chatbot.models import ChatbotConversation


class Command(BaseCommand):
    help = "Supprime les conversations du chatbot plus anciennes que la durée de conservation RGPD (180 jours par défaut)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=180,
            help="Nombre de jours de conservation (défaut: 180 jours / 6 mois).",
        )

    def handle(self, *args, **options):
        days = options["days"]
        cutoff = timezone.now() - timedelta(days=days)
        deleted_count, _ = ChatbotConversation.objects.filter(updated_at__lt=cutoff).delete()
        self.stdout.write(
            self.style.SUCCESS(
                f"{deleted_count} conversation(s) du chatbot antérieure(s) à {days} jours supprimée(s)."
            )
        )
