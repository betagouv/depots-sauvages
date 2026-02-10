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
