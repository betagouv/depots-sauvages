import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from backend.proconnect.models import ProConnectAccessConfig
from backend.unit_tests.factories import UserFactory


@pytest.mark.django_db
def test_proconnect_access_config_permissions():
    client = APIClient()
    url = reverse("backoffice-proconnect-config")
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    regular_user = UserFactory(is_staff=False)
    client.force_authenticate(user=regular_user)
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    staff_user = UserFactory(is_staff=True)
    client.force_authenticate(user=staff_user)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_proconnect_access_config_get_and_put():
    staff_user = UserFactory(is_staff=True)
    client = APIClient()
    client.force_authenticate(user=staff_user)
    url = reverse("backoffice-proconnect-config")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "categories_juridiques_autorisees" in data
    assert "sirens_autorises" in data
    new_payload = {
        "categories_juridiques_autorisees": [
            {"code": "72", "nom": "Communes"},
            {"code": "734", "nom": "Intercommunalités"},
        ],
        "sirens_autorises": [
            {"siren": "157000019", "nom": "Gendarmerie"},
            {"siren": "662043116", "nom": "ONF"},
        ],
    }
    put_response = client.put(url, new_payload, format="json")
    assert put_response.status_code == status.HTTP_200_OK
    assert len(put_response.json()["sirens_autorises"]) == 2
    config = ProConnectAccessConfig.get_solo()
    assert config.est_siren_autorise("157000019") is True
    assert config.est_siren_autorise("999999999") is False
    assert config.est_categorie_juridique_autorisee("7210") is True
    assert config.est_categorie_juridique_autorisee("5499") is False


@pytest.mark.django_db
def test_proconnect_access_config_validation_error():
    staff_user = UserFactory(is_staff=True)
    client = APIClient()
    client.force_authenticate(user=staff_user)
    url = reverse("backoffice-proconnect-config")
    invalid_siren_payload = {
        "categories_juridiques_autorisees": [],
        "sirens_autorises": [{"siren": "invalid-123", "nom": "Mauvais"}],
    }
    response = client.put(url, invalid_siren_payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    invalid_cat_payload = {
        "categories_juridiques_autorisees": [{"code": "ABC", "nom": "Mauvais code"}],
        "sirens_autorises": [],
    }
    response = client.put(url, invalid_cat_payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_proconnect_access_config_duplicate_error():
    staff_user = UserFactory(is_staff=True)
    client = APIClient()
    client.force_authenticate(user=staff_user)
    url = reverse("backoffice-proconnect-config")
    duplicate_siren_payload = {
        "categories_juridiques_autorisees": [],
        "sirens_autorises": [
            {"siren": "157000019", "nom": "Gendarmerie 1"},
            {"siren": "157000019", "nom": "Gendarmerie 2"},
        ],
    }
    response = client.put(url, duplicate_siren_payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "sirens_autorises" in data
    assert any("en double" in str(err) for err in data["sirens_autorises"])


@pytest.mark.django_db
def test_proconnect_access_config_max_length_validation():
    staff_user = UserFactory(is_staff=True)
    client = APIClient()
    client.force_authenticate(user=staff_user)
    url = reverse("backoffice-proconnect-config")
    long_code_payload = {
        "categories_juridiques_autorisees": [{"code": "12345678901", "nom": "Trop long"}],
        "sirens_autorises": [],
    }
    response = client.put(url, long_code_payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    long_nom_payload = {
        "categories_juridiques_autorisees": [],
        "sirens_autorises": [{"siren": "157000019", "nom": "A" * 256}],
    }
    response = client.put(url, long_nom_payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
