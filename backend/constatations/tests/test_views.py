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


@pytest.mark.django_db
def test_update_constatation_prejudice(client):
    user = UserFactory()
    client.force_login(user)
    # Create initial constatation
    constatation = Constatation.objects.create(
        user=user,
        commune="Paris",
        plainte_etat="Déposée",
        prejudice_montant_connu=False,
        prejudice_nombre_personnes=5,
        prejudice_nombre_heures=2,
    )
    url = reverse("constatation-detail", args=[constatation.id])
    # Update to prejudice_montant_connu = True
    data = {
        "commune": "Paris",
        "plainte_etat": "Déposée",
        "prejudice_montant_connu": True,
        "prejudice_montant": 500,
        "prejudice_nombre_personnes": None,
        "prejudice_nombre_heures": None,
        "prejudice_nombre_vehicules": None,
        "prejudice_kilometrage": None,
        "prejudice_autres_couts": None,
    }
    response = client.put(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    constatation.refresh_from_db()
    assert constatation.prejudice_montant_connu is True
    assert constatation.prejudice_montant == 500
    assert constatation.prejudice_nombre_personnes is None

