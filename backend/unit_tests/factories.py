import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True  # Fix a warning

    username = factory.Faker("user_name")
    email = factory.Faker("email")

    @factory.post_generation
    def team(obj, create, extracted, **kwargs):
        if not create:
            return
        from backend.teams.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=obj)
        if extracted is not None:
            profile.team = extracted
            profile.save(update_fields=["team"])

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        password = extracted or "password"
        obj.set_password(password)
        if create:
            obj.save()
