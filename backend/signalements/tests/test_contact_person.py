import pytest
from django.conf import settings
from django.urls import reverse

from backend.signalements.models import Signalement
from backend.unit_tests.factories import SignalementFactory

pytestmark = pytest.mark.django_db(databases=settings.DATABASES.keys())


def test_that_contact_fields_are_included_in_api_list_endpoint(client):
    SignalementFactory(
        commune="Contact Test Commune",
        contact_nom="Dupont",
        contact_prenom="Jean",
        contact_email="jean.dupont@example.com",
        contact_telephone="0123456789",
        accepte_accompagnement=True,
    )
    url = reverse("signalement-list")
    response = client.get(url)
    response_data = response.json()
    assert "Dupont" in str(response_data)
    assert "Jean" in str(response_data)
    assert "jean.dupont@example.com" in str(response_data)
    assert "0123456789" in str(response_data)


def test_that_contact_fields_are_created_via_api_create_endpoint(client):
    url = reverse("signalement-list")
    data = {
        "commune": "New Contact Commune",
        "date_constat": "2025-01-01",
        "heure_constat": "14:30:00",
        "contact_nom": "Dupont",
        "contact_prenom": "Marie",
        "contact_email": "marie.dupont@example.com",
        "contact_telephone": "0987654321",
        "accepte_accompagnement": False,
    }
    assert not Signalement.objects.filter(commune="New Contact Commune").exists()
    response = client.post(url, data, content_type="application/json")
    assert Signalement.objects.filter(commune="New Contact Commune").exists()
    response_data = response.json()
    assert "Dupont" in str(response_data)
    assert "Marie" in str(response_data)
    assert "marie.dupont@example.com" in str(response_data)
    assert "0987654321" in str(response_data)


def test_that_contact_fields_are_retrieved_via_api_detail_endpoint(client):
    signalement = SignalementFactory(
        commune="Retrieve Contact Commune",
        contact_nom="Dupont",
        contact_prenom="Pierre",
        contact_email="pierre.dupont@example.com",
    )
    url = reverse("signalement-detail", kwargs={"pk": signalement.id})
    response = client.get(url)
    response_data = response.json()
    assert "Dupont" in str(response_data)
    assert "Pierre" in str(response_data)
    assert "pierre.dupont@example.com" in str(response_data)


def test_that_contact_fields_are_updated_via_api_update_endpoint(client):
    signalement = SignalementFactory(
        commune="Update Contact Commune",
        contact_nom="Original",
        contact_email="original@example.com",
    )
    url = reverse("signalement-detail", kwargs={"pk": signalement.id})
    data = {
        "commune": "Update Contact Commune",
        "date_constat": "2025-02-01",
        "heure_constat": "15:45:00",
        "contact_nom": "Updated",
        "contact_prenom": "Contact",
        "contact_email": "updated@example.com",
        "contact_telephone": "0555666777",
        "accepte_accompagnement": True,
    }
    response = client.put(url, data, content_type="application/json")
    response_data = response.json()
    assert "Updated" in str(response_data)
    assert "Contact" in str(response_data)
    assert "updated@example.com" in str(response_data)
    assert "0555666777" in str(response_data)
    signalement.refresh_from_db()
    assert signalement.contact_nom == "Updated"
    assert signalement.contact_prenom == "Contact"
    assert signalement.contact_email == "updated@example.com"
