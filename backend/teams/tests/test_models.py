import pytest
from django.contrib.auth import get_user_model
from backend.teams.models import Team, TeamAutoCreationExclusion, UserProfile, get_user_team
from backend.constatations.models import Constatation
from backend.procedures.models import SuiviProcedure

User = get_user_model()


@pytest.mark.django_db
def test_create_team_and_link_user():
    team = Team.objects.create(name="Mairie de Test", siret="12345678901234", siren="123456789")
    user = User.objects.create_user(username="agent1", email="agent1@test.fr")

    profile, _ = UserProfile.objects.get_or_create(user=user)
    assert profile.team is None
    assert get_user_team(user) is None

    profile.team = team
    profile.save()

    assert get_user_team(user) == team
    assert team.members.count() == 1
    assert team.members.first().user == user


@pytest.mark.django_db
def test_create_team_autocreation_exclusion():
    exclusion = TeamAutoCreationExclusion.objects.create(
        siren="157000019",
        label="Gendarmerie Nationale",
        reason="Corps national",
    )
    assert str(exclusion) == "Gendarmerie Nationale (157000019)"
    assert TeamAutoCreationExclusion.objects.filter(siren="157000019").exists()


@pytest.mark.django_db
def test_constatation_team_and_traceability_fields():
    team = Team.objects.create(name="Police Municipale", siret="98765432109876", siren="987654321")
    alice = User.objects.create_user(username="alice", email="alice@test.fr")
    bob = User.objects.create_user(username="bob", email="bob@test.fr")
    UserProfile.objects.create(user=alice, team=team)
    UserProfile.objects.create(user=bob, team=team)

    constatation = Constatation.objects.create(
        user=alice,
        created_by=alice,
        updated_by=bob,
        team=team,
        commune="Testville",
    )

    assert constatation.team == team
    assert constatation.created_by == alice
    assert constatation.updated_by == bob
    assert team.constatations.count() == 1

    # SuiviProcedure was automatically created by signal and tracks updates
    suivi = constatation.suivi_procedure
    suivi.updated_by = bob
    suivi.save()

    assert suivi.updated_by == bob
    assert bob.suivis_modifies.count() == 1
