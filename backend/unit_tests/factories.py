import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

from backend.signalements.models import Signalement

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")


class SignalementFactory(factory.django.DjangoModelFactory):
    """Factory for creating Signalement instances for testing."""

    class Meta:
        model = Signalement

    commune = factory.Faker("city")
    date_constat = factory.LazyFunction(lambda: timezone.now().date())
    heure_constat = factory.LazyFunction(lambda: timezone.now().time())
    prejudice_montant_connu = False
    prejudice_nombre_personnes = 1
    prejudice_nombre_heures = 1
    prejudice_nombre_vehicules = 1
    prejudice_kilometrage = 10
    prejudice_autres_couts = 0
    contact_nom = factory.Faker("last_name")
    contact_prenom = factory.Faker("first_name")
    contact_email = factory.Faker("email")
    contact_telephone = factory.Faker("phone_number")
    accepte_accompagnement = factory.Faker("boolean")


class DNSignalementFactory(SignalementFactory):
    """Factory for creating DNSignalement instances for testing."""

    class Meta:
        model = "dn_signalements.DNSignalement"

    dn_numero_dossier = factory.Sequence(lambda n: n + 10000)
