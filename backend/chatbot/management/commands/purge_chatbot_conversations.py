from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from backend.chatbot.models import ChatbotConversation


class Command(BaseCommand):
    help = (
        "Purges chatbot conversations older than the GDPR retention period (180 days by default)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=180,
            help="Number of retention days (default: 180 days / 6 months).",
        )

    def handle(self, *args, **options):
        days = options["days"]
        cutoff = timezone.now() - timedelta(days=days)
        deleted_count, _ = ChatbotConversation.objects.filter(updated_at__lt=cutoff).delete()
        self.stdout.write(
            self.style.SUCCESS(
                f"{deleted_count} chatbot conversation(s) older than {days} days deleted."
            )
        )
