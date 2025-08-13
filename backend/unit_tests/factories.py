import factory
from django.utils import timezone

from backend.signalements.models import Signalement


class SignalementFactory(factory.django.DjangoModelFactory):
    """Factory for creating Signalement instances for testing."""

    class Meta:
        model = Signalement

    commune = factory.Faker("city")
    date_constat = factory.LazyFunction(lambda: timezone.now().date())
    heure_constat = factory.LazyFunction(lambda: timezone.now().time())
