import pytest
from django.contrib.auth import get_user_model
from backend.teams.models import Team, TeamAutoCreationExclusion
from backend.constatations.models import Constatation
from backend.procedures.models import SuiviProcedure

User = get_user_model()


@pytest.mark.django_db
def test_create_team_and_link_user():
    team = Team.objects.create(name="Mairie de Test", siret="12345678901234", siren="123456789")
    user = User.objects.create_user(username="agent1", email="agent1@test.fr")

    assert user.team is None

    user.team = team
    user.save()

    assert user.team == team
    assert team.members.count() == 1
    assert team.members.first() == user


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
    alice = User.objects.create_user(username="alice", email="alice@test.fr", team=team)
    bob = User.objects.create_user(username="bob", email="bob@test.fr", team=team)

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

    # SuiviProcedure was automatically created by signal and can track updates
    suivi = constatation.suivi_procedure
    suivi.created_by = alice
    suivi.updated_by = bob
    suivi.save()

    assert suivi.created_by == alice
    assert suivi.updated_by == bob
    assert alice.suivis_crees.count() == 1
    assert bob.suivis_modifies.count() == 1
