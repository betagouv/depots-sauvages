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
def test_user_info_authenticated(client):
    user = UserFactory(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        username="john@example.com",
        is_staff=False,
    )
    client.force_login(user)
    url = reverse("user-info-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_authenticated"] is True
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["email"] == "john@example.com"
    assert data["is_staff"] is False

    # Test with staff user
    staff_user = UserFactory(is_staff=True)
    client.force_login(staff_user)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["is_staff"] is True


@pytest.mark.django_db
def test_user_info_anonymous(client):
    url = reverse("user-info-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_authenticated"] is False
    assert data["is_staff"] is False
    assert "first_name" not in data
    assert "last_name" not in data
    assert "email" not in data


@pytest.mark.django_db
def test_logout_proconnect_user(client, settings):
    settings.PROCONNECT_ENABLED = True
    settings.OIDC_OP_LOGOUT_ENDPOINT = "https://example.com/logout"
    user = UserFactory()
    client.force_login(user, backend="backend.proconnect.auth.ProConnectOIDCBackend")
    # Store token mock in session
    session = client.session
    session["oidc_id_token"] = "mock-id-token"
    session.save()
    url = reverse("logout")
    response = client.get(url)
    assert response.status_code == status.HTTP_302_FOUND
    assert "https://example.com/logout" in response.url
    assert "post_logout_redirect_uri" in response.url
    assert "id_token_hint=mock-id-token" in response.url


@pytest.mark.django_db
def test_logout_bypass_auth_user(client, settings):
    settings.PROCONNECT_ENABLED = True
    settings.OIDC_OP_LOGOUT_ENDPOINT = "https://example.com/logout"
    user = UserFactory()
    client.force_login(user, backend="backend.bypass_auth.auth.BypassAuthBackend")
    url = reverse("logout")
    response = client.get(url)
    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == reverse("index")


@pytest.mark.django_db
def test_logout_standard_user(client, settings):
    settings.PROCONNECT_ENABLED = True
    settings.OIDC_OP_LOGOUT_ENDPOINT = "https://example.com/logout"
    user = UserFactory()
    client.force_login(user)
    url = reverse("logout")
    response = client.get(url)
    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == reverse("index")


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


@pytest.mark.django_db
@pytest.mark.parametrize("env", ["staging", "dev", "local", "development"])
def test_robots_txt_non_prod(client, settings, env):
    settings.ENV_NAME = env
    response = client.get(reverse("robots_txt"))
    assert response.status_code == 200
    assert "text/plain" in response["Content-Type"]
    content = response.content.decode()
    assert "Allow: /" in content
    assert "Disallow: /" not in content


@pytest.mark.django_db
def test_robots_txt_prod(client, settings):
    settings.ENV_NAME = "prod"
    settings.ADMIN_URL_NAME = "my-custom-admin-portal"
    response = client.get(reverse("robots_txt"))
    assert response.status_code == 200
    assert "text/plain" in response["Content-Type"]
    content = response.content.decode()
    assert "Disallow: /my-custom-admin-portal/" in content
    assert "Allow: /" in content


@pytest.mark.django_db
@pytest.mark.parametrize("env", ["staging", "dev", "local", "development"])
def test_middleware_non_prod_headers(client, settings, env):
    settings.ENV_NAME = env
    response = client.get(reverse("index"))
    assert response["X-Robots-Tag"] == "noindex, nofollow"


@pytest.mark.django_db
def test_middleware_prod_headers(client, settings):
    settings.ENV_NAME = "prod"
    response = client.get(reverse("index"))
    assert "X-Robots-Tag" not in response


@pytest.mark.django_db
@pytest.mark.parametrize("env", ["staging", "dev", "local", "development"])
def test_seo_robots_meta_non_prod(client, settings, env):
    settings.ENV_NAME = env
    response = client.get(reverse("index"))
    assert response.status_code == 200
    content = response.content.decode()
    assert '<meta name="robots" content="noindex, nofollow" />' in content


@pytest.mark.django_db
def test_seo_robots_meta_prod(client, settings):
    settings.ENV_NAME = "prod"
    response = client.get(reverse("index"))
    assert response.status_code == 200
    content = response.content.decode()
    assert '<meta name="robots" content="index, follow" />' in content
