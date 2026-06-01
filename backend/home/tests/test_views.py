import pytest
from django.urls import reverse
from rest_framework import status

from backend.unit_tests.factories import UserFactory


@pytest.mark.django_db
def test_home_page_loads_correctly(client):
    url = reverse("index")
    response = client.get(url)
    assert "Protect'Envi" in response.content.decode()


@pytest.mark.django_db
def test_user_info_authenticated(client):
    user = UserFactory(
        first_name="John", last_name="Doe", email="john@example.com", username="john@example.com"
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


@pytest.mark.django_db
def test_user_info_anonymous(client):
    url = reverse("user-info-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_authenticated"] is False
    assert "first_name" not in data
    assert "last_name" not in data
    assert "email" not in data


@pytest.mark.django_db
def test_logout_proconnect_user(client, settings):
    settings.PROCONNECT_ENABLED = True
    settings.OIDC_OP_LOGOUT_ENDPOINT = "https://example.com/logout"
    user = UserFactory()
    client.force_login(user, backend="backend.home.auth.ProConnectOIDCBackend")
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
