import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from backend.proconnect.auth import ProConnectOIDCBackend
from backend.unit_tests.factories import UserFactory


@pytest.mark.django_db
def test_home_page_loads_correctly(client):
    url = reverse("index")
    response = client.get(url)
    content = response.content.decode()
    assert "Protect’Envi" in content or "Protect&#x27;Envi" in content


@pytest.mark.django_db
def test_proconnect_oidc_backend_claims(settings):
    settings.OIDC_OP_TOKEN_ENDPOINT = "https://example.com/token"
    settings.OIDC_OP_USER_ENDPOINT = "https://example.com/userinfo"
    settings.OIDC_OP_JWKS_ENDPOINT = "https://example.com/jwks"
    settings.OIDC_RP_CLIENT_ID = "mock-client"
    settings.OIDC_RP_CLIENT_SECRET = "mock-secret"
    settings.OIDC_RP_SIGN_ALGO = "RS256"

    User = get_user_model()
    backend = ProConnectOIDCBackend()
    user = User.objects.create(username="agent@example.com", email="agent@example.com")
    # Test update_user with usual_name
    claims = {
        "email": "agent@example.com",
        "given_name": "Jean",
        "family_name": "Dupont",
        "usual_name": "Martin",
    }
    updated_user = backend.update_user(user, claims)
    assert updated_user.first_name == "Jean"
    assert updated_user.last_name == "Martin"

    # Test update_user with family_name fallback (no usual_name)
    claims_no_usual = {
        "email": "agent@example.com",
        "given_name": "Jean-Pierre",
        "family_name": "Dupont-Deschamps",
    }
    updated_user_no_usual = backend.update_user(user, claims_no_usual)
    assert updated_user_no_usual.first_name == "Jean-Pierre"
    assert updated_user_no_usual.last_name == "Dupont-Deschamps"
