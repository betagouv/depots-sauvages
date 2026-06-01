import pytest
from django.urls import reverse
from rest_framework import status

from backend.constatations.models import Constatation
from backend.unit_tests.factories import UserFactory


@pytest.mark.django_db
def test_create_constatation_authenticated(client):
    user = UserFactory()
    client.force_login(user)
    url = reverse("constatation-list")
    data = {
        "commune": "Paris",
        "auteur_identifie": True,
    }
    response = client.post(url, data, format="json")
    # Let's check the response status and the database
    assert response.status_code == status.HTTP_201_CREATED
    constatation = Constatation.objects.first()
    assert constatation is not None
    assert constatation.user == user
    assert constatation.commune == "Paris"


@pytest.mark.django_db
def test_create_constatation_anonymous(client):
    url = reverse("constatation-list")
    data = {
        "commune": "Paris",
        "auteur_identifie": True,
    }
    response = client.post(url, data, format="json")
    # Unauthenticated requests should be rejected
    assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    assert Constatation.objects.count() == 0
