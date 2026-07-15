import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from backend.unit_tests.factories import UserFactory

User = get_user_model()


@pytest.fixture
def test_users(db):
    regular_user = UserFactory(
        username="user@example.com",
        email="user@example.com",
        first_name="Jean",
        last_name="Dupont",
    )
    staff_user = UserFactory(
        username="staff@example.com",
        email="staff@example.com",
        first_name="Staff",
        last_name="Member",
        is_staff=True,
    )
    superuser = UserFactory(
        username="admin@example.com",
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        is_superuser=True,
    )
    return regular_user, staff_user, superuser


@pytest.mark.django_db
def test_disabled_by_default(client, settings, test_users):
    regular_user, staff_user, superuser = test_users
    settings.BYPASS_AUTH_ENABLED = False
    # Config should return 404 when disabled
    config_url = reverse("bypass-auth-config")
    response = client.get(config_url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # Login endpoint should return 404 when disabled
    login_url = reverse("bypass-auth-login")
    response = client.post(login_url, {"email": regular_user.username})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_login_success_for_regular_user(client, settings, test_users):
    regular_user, staff_user, superuser = test_users
    settings.BYPASS_AUTH_ENABLED = True
    login_url = reverse("bypass-auth-login")
    response = client.post(login_url, {"email": regular_user.username})
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "Successfully logged in via bypass"
    assert response.data["user"]["id"] == regular_user.id
    # Check that user is indeed logged in to the session
    user_info_url = reverse("user-info-list")
    response = client.get(user_info_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["is_authenticated"] is True
    assert response.data["email"] == "user@example.com"


@pytest.mark.django_db
def test_login_denied_for_privileged_users(client, settings, test_users):
    regular_user, staff_user, superuser = test_users
    settings.BYPASS_AUTH_ENABLED = True
    login_url = reverse("bypass-auth-login")
    # Try staff
    response = client.post(login_url, {"email": staff_user.username})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    # Try superuser
    response = client.post(login_url, {"email": superuser.username})
    assert response.status_code == status.HTTP_403_FORBIDDEN
