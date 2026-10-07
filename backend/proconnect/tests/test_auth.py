from unittest.mock import MagicMock, patch

import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.management import call_command
from django.test import RequestFactory

from backend.proconnect.auth import ProConnectOIDCBackend, get_nature_juridique_for_siren


@pytest.fixture(autouse=True)
def load_proconnect_fixture(db):
    call_command("loaddata", "proconnect_access_config")


def create_request_with_session():
    factory = RequestFactory()
    request = factory.get("/authenticate/")
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()
    return request


@pytest.mark.django_db
def test_proconnect_profile_sync_on_create_and_update(settings):
    settings.OIDC_OP_TOKEN_ENDPOINT = "https://example.com/token"
    settings.OIDC_OP_USER_ENDPOINT = "https://example.com/userinfo"
    settings.OIDC_OP_JWKS_ENDPOINT = "https://example.com/jwks"
    settings.OIDC_RP_CLIENT_ID = "mock-client"
    settings.OIDC_RP_CLIENT_SECRET = "mock-secret"
    settings.OIDC_RP_SIGN_ALGO = "RS256"

    backend = ProConnectOIDCBackend()
    claims = {
        "sub": "user-sub-12345",
        "email": "agent.test@mairie.fr",
        "given_name": "Claire",
        "family_name": "Dupont",
        "usual_name": "Martin",
        "siret": "21750001600019",
        "organization_label": "Mairie de Test",
        "roles": ["agent_public", "agent_public_territorial"],
    }
    user = backend.create_user(claims)
    assert user.email == "agent.test@mairie.fr"
    assert user.first_name == "Claire"
    assert user.last_name == "Martin"
    assert hasattr(user, "proconnect_profile")
    profile = user.proconnect_profile
    assert profile.sub == "user-sub-12345"
    assert profile.siret == "21750001600019"
    assert profile.siren == "217500016"
    assert profile.organization_label == "Mairie de Test"
    assert profile.roles == ["agent_public", "agent_public_territorial"]
    assert profile.raw_claims["sub"] == "user-sub-12345"
    assert profile.raw_claims["siret"] == "21750001600019"

    # Test update_user updates existing profile
    updated_claims = {
        "sub": "user-sub-12345",
        "email": "agent.test@mairie.fr",
        "given_name": "Claire",
        "family_name": "Dupont",
        "usual_name": "Martin-Duval",
        "siret": "21750001699999",
        "organization_label": "Mairie Centrale",
        "roles": ["agent_public"],
    }
    updated_user = backend.update_user(user, updated_claims)
    profile.refresh_from_db()
    assert updated_user.last_name == "Martin-Duval"
    assert profile.siret == "21750001699999"
    assert profile.siren == "217500016"
    assert profile.organization_label == "Mairie Centrale"
    assert profile.roles == ["agent_public"]


@pytest.mark.django_db
def test_proconnect_profile_sync_with_missing_claims(settings):
    settings.OIDC_OP_TOKEN_ENDPOINT = "https://example.com/token"
    settings.OIDC_OP_USER_ENDPOINT = "https://example.com/userinfo"
    settings.OIDC_OP_JWKS_ENDPOINT = "https://example.com/jwks"
    settings.OIDC_RP_CLIENT_ID = "mock-client"
    settings.OIDC_RP_CLIENT_SECRET = "mock-secret"
    settings.OIDC_RP_SIGN_ALGO = "RS256"

    backend = ProConnectOIDCBackend()
    claims = {
        "sub": "user-sub-67890",
        "email": "agent.sans.orga@example.com",
        "given_name": "Paul",
    }
    user = backend.create_user(claims)
    profile = user.proconnect_profile
    assert profile.sub == "user-sub-67890"
    assert profile.siret == ""
    assert profile.siren == ""
    assert profile.organization_label == ""
    assert profile.roles == []
    assert profile.raw_claims == claims


@pytest.mark.django_db
def test_is_eligible_rejected_if_not_agent_public():
    backend = ProConnectOIDCBackend()
    claims = {
        "roles": ["particulier"],
        "siret": "21750001600019",
    }
    assert backend.is_eligible_proconnect_user(claims) is False


@pytest.mark.django_db
def test_is_eligible_rejected_if_no_siret_or_siren():
    backend = ProConnectOIDCBackend()
    claims = {
        "roles": ["agent_public"],
        "siret": "",
    }
    assert backend.is_eligible_proconnect_user(claims) is False


@pytest.mark.django_db
def test_is_eligible_accepted_for_whitelisted_state_siren():
    backend = ProConnectOIDCBackend()
    # 157000019 is Gendarmerie (in sirens_autorises fixture)
    claims = {
        "roles": ["agent_public", "agent_public_etat"],
        "siret": "15700001900461",
        "organization_label": "Direction générale de la gendarmerie nationale",
    }
    assert backend.is_eligible_proconnect_user(claims) is True


@pytest.mark.django_db
def test_is_eligible_accepted_for_allowed_legal_category():
    backend = ProConnectOIDCBackend()
    claims = {
        "roles": ["agent_public", "agent_public_territorial"],
        "siret": "21871060600011",
        "organization_label": "Commune de Nexon",
    }
    with patch("backend.proconnect.auth.get_nature_juridique_for_siren", return_value="7210"):
        assert backend.is_eligible_proconnect_user(claims) is True


@pytest.mark.django_db
def test_is_eligible_rejected_for_unauthorized_legal_category():
    backend = ProConnectOIDCBackend()
    claims = {
        "roles": ["agent_public", "agent_public_etat"],
        "siret": "19753471000014",
        "organization_label": "Rectorat de Paris",
    }
    # 7331 is middle schools / academy / rectorate (not in allowed prefixes)
    with patch("backend.proconnect.auth.get_nature_juridique_for_siren", return_value="7331"):
        assert backend.is_eligible_proconnect_user(claims) is False


@pytest.mark.django_db
def test_get_or_create_user_rejected_stores_session_info():

    backend = ProConnectOIDCBackend()
    request = create_request_with_session()
    backend.request = request

    user_info = {
        "sub": "non-eligible-sub",
        "email": "agent@rectorat.fr",
        "given_name": "Jean",
        "family_name": "Valjean",
        "siret": "19753471000014",
        "organization_label": "Rectorat de Paris",
        "roles": ["agent_public"],
    }

    with patch.object(backend, "get_userinfo", return_value=user_info):
        with patch("backend.proconnect.auth.get_nature_juridique_for_siren", return_value="7331"):
            user = backend.get_or_create_user("fake_access_token", "fake_id_token", {})
            assert user is None
            assert "proconnect_rejected_info" in request.session
            rejected = request.session["proconnect_rejected_info"]
            assert rejected["siret"] == "19753471000014"
            assert rejected["siren"] == "197534710"
            assert rejected["organization_label"] == "Rectorat de Paris"
            assert rejected["email"] == "agent@rectorat.fr"
            assert rejected["name"] == "Jean Valjean"


@pytest.mark.django_db
def test_get_nature_juridique_for_siren_api_success():
    fake_response = MagicMock()
    fake_response.read.return_value = b'{"results": [{"nature_juridique": "7210"}]}'
    fake_response.__enter__.return_value = fake_response

    with patch("urllib.request.urlopen", return_value=fake_response):
        nature = get_nature_juridique_for_siren("218710606")
        assert nature == "7210"


@pytest.mark.django_db
def test_get_nature_juridique_for_siren_api_error_returns_empty_string():
    with patch("urllib.request.urlopen", side_effect=Exception("API timeout")):
        nature = get_nature_juridique_for_siren("218710606")
        assert nature == ""


@pytest.mark.django_db
def test_proconnect_auth_uses_local_public_entity_without_api_call():
    from backend.proconnect.models import PublicEntitySirene

    PublicEntitySirene.objects.create(
        siren="217500016",
        categorie_juridique="7210",
        denomination="Ville de Paris",
    )
    backend = ProConnectOIDCBackend()
    claims = {
        "roles": ["agent_public"],
        "siret": "21750001600019",
        "organization_label": "Ville de Paris",
    }
    with patch("backend.proconnect.auth.get_nature_juridique_for_siren") as mock_api:
        assert backend.is_eligible_proconnect_user(claims) is True
        mock_api.assert_not_called()


@pytest.mark.django_db
def test_proconnect_auth_fallback_api_caches_in_public_entity():
    from backend.proconnect.models import PublicEntitySirene

    siren = "218710606"
    assert not PublicEntitySirene.objects.filter(siren=siren).exists()
    backend = ProConnectOIDCBackend()
    claims = {
        "roles": ["agent_public"],
        "siret": f"{siren}00011",
        "organization_label": "Mairie Inconnue",
    }
    fake_response = MagicMock()
    fake_response.read.return_value = (
        b'{"results": [{"nature_juridique": "7210", "nom_complet": "Mairie Inconnue"}]}'
    )
    fake_response.__enter__.return_value = fake_response
    with patch("urllib.request.urlopen", return_value=fake_response):
        assert backend.is_eligible_proconnect_user(claims) is True
    cached = PublicEntitySirene.objects.filter(siren=siren).first()
    assert cached is not None
    assert cached.categorie_juridique == "7210"
    assert cached.denomination == "Mairie Inconnue"


@pytest.mark.django_db
def test_is_eligible_when_restrictions_disabled(settings):
    settings.PROCONNECT_ACCESS_RESTRICTIONS_ENABLED = False
    backend = ProConnectOIDCBackend()
    unauthorized_claims = {
        "roles": ["particulier"],
        "siret": "",
    }
    assert backend.is_eligible_proconnect_user(unauthorized_claims) is True
