import pytest
from backend.proconnect.auth import ProConnectOIDCBackend


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
