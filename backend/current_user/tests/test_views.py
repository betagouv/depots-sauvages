import pytest
from django.urls import reverse
from rest_framework import status

from backend.constatations.models import Constatation
from backend.teams.models import Team
from backend.unit_tests.factories import UserFactory


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
    assert data["team_id"] is None
    assert data["team_name"] is None
    assert data["team_logo"] is None
    assert data["team_siret"] is None
    assert data["procedures_count"] == 0
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
def test_user_info_with_team_and_procedures_count(client):
    team = Team.objects.create(name="Mairie de Lyon", siret="12345678901234", siren="123456789")
    alice = UserFactory(team=team)
    bob = UserFactory(team=team)
    solo_user = UserFactory()

    # Create 2 constatations for team, 1 for solo user
    Constatation.objects.create(user=alice, created_by=alice, team=team, commune="Lyon 1")
    Constatation.objects.create(user=bob, created_by=bob, team=team, commune="Lyon 2")
    Constatation.objects.create(user=solo_user, created_by=solo_user, team=None, commune="Solo 1")

    # Bob logs in: procedures_count should be 2 (both team constatations)
    client.force_login(bob)
    response = client.get(reverse("user-info-list"))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["team_id"] == team.id
    assert data["team_name"] == "Mairie de Lyon"
    assert data["team_siret"] == "12345678901234"
    assert data["team_logo"] is None
    assert data["procedures_count"] == 2

    # Solo user logs in: procedures_count should be 1
    client.force_login(solo_user)
    res_solo = client.get(reverse("user-info-list"))
    assert res_solo.status_code == status.HTTP_200_OK
    data_solo = res_solo.json()
    assert data_solo["team_id"] is None
    assert data_solo["team_name"] is None
    assert data_solo["team_siret"] is None
    assert data_solo["procedures_count"] == 1


@pytest.mark.django_db
def test_user_info_inactive_user(client):
    user = UserFactory(is_active=False)
    client.force_login(user)
    response = client.get(reverse("user-info-list"))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_authenticated"] is False
