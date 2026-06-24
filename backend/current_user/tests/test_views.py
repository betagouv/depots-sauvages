import pytest
from django.urls import reverse
from rest_framework import status

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
