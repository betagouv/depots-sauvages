import pytest
from django.contrib.auth import get_user_model

from backend.constatations.models import Constatation
from backend.proconnect.auth import ProConnectOIDCBackend, sync_proconnect_team
from backend.teams.models import Team, TeamAutoCreationExclusion, UserProfile, get_user_team

User = get_user_model()


@pytest.fixture(autouse=True)
def setup_proconnect_settings(settings):
    settings.OIDC_OP_TOKEN_ENDPOINT = "https://example.com/token"
    settings.OIDC_OP_USER_ENDPOINT = "https://example.com/userinfo"
    settings.OIDC_OP_JWKS_ENDPOINT = "https://example.com/jwks"
    settings.OIDC_RP_CLIENT_ID = "mock-client"
    settings.OIDC_RP_CLIENT_SECRET = "mock-secret"
    settings.OIDC_RP_SIGN_ALGO = "RS256"


@pytest.mark.django_db
def test_eligible_user_creates_and_attaches_to_new_team():
    backend = ProConnectOIDCBackend()
    claims = {
        "sub": "sub-agent-1",
        "email": "agent1@commune.fr",
        "given_name": "Jean",
        "family_name": "Valjean",
        "siret": "21750001600019",
        "organization_label": "Mairie de Paris",
        "roles": ["agent_public"],
    }
    user = backend.create_user(claims)

    user.refresh_from_db()
    assert get_user_team(user) is not None
    assert get_user_team(user).siret == "21750001600019"
    assert get_user_team(user).siren == "217500016"
    assert get_user_team(user).name == "Mairie de Paris"
    assert get_user_team(user).members.filter(user=user).exists()


@pytest.mark.django_db
def test_colleague_joins_existing_team():
    backend = ProConnectOIDCBackend()
    claims_user1 = {
        "sub": "sub-agent-1",
        "email": "agent1@commune.fr",
        "given_name": "Jean",
        "family_name": "Valjean",
        "siret": "21750001600019",
        "organization_label": "Mairie de Paris",
        "roles": ["agent_public"],
    }
    user1 = backend.create_user(claims_user1)

    claims_user2 = {
        "sub": "sub-agent-2",
        "email": "agent2@commune.fr",
        "given_name": "Cosette",
        "family_name": "Fauchelevent",
        "siret": "21750001600019",
        "organization_label": "Mairie de Paris",
        "roles": ["agent_public"],
    }
    user2 = backend.create_user(claims_user2)

    user1.refresh_from_db()
    user2.refresh_from_db()

    assert get_user_team(user1) == get_user_team(user2)
    assert Team.objects.filter(siret="21750001600019").count() == 1
    assert get_user_team(user1).members.count() == 2


@pytest.mark.django_db
def test_user_with_fallback_name_when_org_label_missing():
    backend = ProConnectOIDCBackend()
    claims = {
        "sub": "sub-agent-no-label",
        "email": "agent@village.fr",
        "given_name": "Pierre",
        "family_name": "Dupont",
        "siret": "21110001600025",
        "organization_label": "",
        "roles": ["agent_public"],
    }
    user = backend.create_user(claims)
    user.refresh_from_db()

    assert get_user_team(user) is not None
    assert get_user_team(user).siret == "21110001600025"
    assert get_user_team(user).name == "Organisation 21110001600025"


@pytest.mark.django_db
def test_orphan_constatations_are_attached_to_newly_joined_team():
    user = User.objects.create_user(username="agent_orphan", email="orphan@commune.fr")
    assert get_user_team(user) is None

    # Create prior orphan constatations
    c1 = Constatation.objects.create(user=user, commune="Village A", team=None)
    c2 = Constatation.objects.create(user=user, commune="Village B", team=None)

    # Another user's constatation (should not be touched)
    other_user = User.objects.create_user(username="other", email="other@other.fr")
    c_other = Constatation.objects.create(user=other_user, commune="Village C", team=None)

    claims = {
        "sub": "sub-orphan-user",
        "email": "orphan@commune.fr",
        "siret": "21750001600019",
        "organization_label": "Mairie de Paris",
    }
    sync_proconnect_team(user, claims)

    user.refresh_from_db()
    c1.refresh_from_db()
    c2.refresh_from_db()
    c_other.refresh_from_db()

    assert get_user_team(user) is not None
    assert c1.team == get_user_team(user)
    assert c2.team == get_user_team(user)
    assert c_other.team is None


@pytest.mark.django_db
def test_user_with_excluded_siren_remains_individual():
    # Exclusion by SIREN (e.g. 157000019 DGGN)
    TeamAutoCreationExclusion.objects.create(
        siren="157000019",
        label="Direction Générale de la Gendarmerie Nationale",
    )

    backend = ProConnectOIDCBackend()
    claims = {
        "sub": "sub-gendarme",
        "email": "gendarme@gendarmerie.interieur.gouv.fr",
        "given_name": "Gérard",
        "family_name": "Lambert",
        "siret": "15700001900012",
        "organization_label": "Brigade Territoriale",
        "roles": ["agent_public"],
    }
    user = backend.create_user(claims)
    user.refresh_from_db()

    assert get_user_team(user) is None
    assert not Team.objects.filter(siret="15700001900012").exists()


@pytest.mark.django_db
def test_user_with_excluded_siret_remains_individual():
    # Exclusion by SIREN (matching the SIRET's first 9 digits)
    TeamAutoCreationExclusion.objects.create(
        siren="130025265",
        label="DINUM",
    )

    backend = ProConnectOIDCBackend()
    claims = {
        "sub": "sub-dinum",
        "email": "agent@dinum.gouv.fr",
        "siret": "13002526500013",
        "organization_label": "DINUM",
        "roles": ["agent_public"],
    }
    user = backend.create_user(claims)
    user.refresh_from_db()

    assert get_user_team(user) is None
    assert not Team.objects.filter(siret="13002526500013").exists()


@pytest.mark.django_db
def test_user_without_valid_siret_remains_individual():
    backend = ProConnectOIDCBackend()

    # Empty siret
    claims_empty = {
        "sub": "sub-nosiret",
        "email": "nosiret@example.com",
        "siret": "",
        "roles": ["agent_public"],
    }
    user_empty = backend.create_user(claims_empty)
    user_empty.refresh_from_db()
    assert get_user_team(user_empty) is None

    # Invalid siret length
    claims_invalid_len = {
        "sub": "sub-invalid-len",
        "email": "invalidlen@example.com",
        "siret": "12345",
        "roles": ["agent_public"],
    }
    user_invalid = backend.create_user(claims_invalid_len)
    user_invalid.refresh_from_db()
    assert get_user_team(user_invalid) is None

    # Non-digit siret
    claims_non_digit = {
        "sub": "sub-nondigit",
        "email": "nondigit@example.com",
        "siret": "1234567890ABCD",
        "roles": ["agent_public"],
    }
    user_non_digit = backend.create_user(claims_non_digit)
    user_non_digit.refresh_from_db()
    assert get_user_team(user_non_digit) is None


@pytest.mark.django_db
def test_user_already_having_team_is_not_reassigned():
    initial_team = Team.objects.create(
        name="Ancienne Mairie",
        siret="11111111111111",
        siren="111111111",
    )
    user = User.objects.create_user(
        username="agent_mutated",
        email="agent@mutation.fr",
    )
    UserProfile.objects.create(user=user, team=initial_team)

    claims_new_org = {
        "sub": "sub-agent-mutated",
        "email": "agent@mutation.fr",
        "siret": "22222222222222",
        "organization_label": "Nouvelle Mairie",
    }
    sync_proconnect_team(user, claims_new_org)

    user.refresh_from_db()
    assert get_user_team(user) == initial_team
    assert not Team.objects.filter(siret="22222222222222").exists()


@pytest.mark.django_db
def test_siret_with_whitespace_is_properly_stripped():
    backend = ProConnectOIDCBackend()
    claims = {
        "sub": "sub-whitespace",
        "email": "agent.spaces@commune.fr",
        "siret": "  21750001600019  ",
        "organization_label": "Mairie avec espaces",
        "roles": ["agent_public"],
    }
    user = backend.create_user(claims)
    user.refresh_from_db()

    assert get_user_team(user) is not None
    assert get_user_team(user).siret == "21750001600019"
    assert get_user_team(user).siren == "217500016"


@pytest.mark.django_db
def test_extremely_long_organization_label_is_safely_truncated():
    backend = ProConnectOIDCBackend()
    long_label = "Direction " + ("A" * 300)
    claims = {
        "sub": "sub-long-label",
        "email": "agent.long@commune.fr",
        "siret": "21750001600099",
        "organization_label": long_label,
        "roles": ["agent_public"],
    }
    user = backend.create_user(claims)
    user.refresh_from_db()

    assert get_user_team(user) is not None
    assert len(get_user_team(user).name) <= 255
    assert get_user_team(user).name == long_label[:255]


@pytest.mark.django_db
def test_orphan_constatations_respect_existing_teams():
    user = User.objects.create_user(username="agent_complex", email="complex@commune.fr")
    other_team = Team.objects.create(
        name="Autre Brigade", siret="99999999999999", siren="999999999"
    )

    # Constatation already associated with another team (should NOT be modified)
    c_existing_team = Constatation.objects.create(
        user=user, commune="Village Protégé", team=other_team
    )
    # Orphan constatation (should be attached)
    c_orphan = Constatation.objects.create(
        user=user, commune="Village Orphelin", team=None
    )

    claims = {
        "sub": "sub-complex",
        "email": "complex@commune.fr",
        "siret": "21750001600019",
        "organization_label": "Mairie de Paris",
    }
    sync_proconnect_team(user, claims)

    c_existing_team.refresh_from_db()
    c_orphan.refresh_from_db()
    user.refresh_from_db()

    assert c_orphan.team == get_user_team(user)
    assert c_existing_team.team == other_team


@pytest.mark.django_db
def test_team_auto_populates_siren_from_siret():
    team = Team.objects.create(name="Auto SIREN", siret="21750001600019")
    assert team.siren == "217500016"
