import pytest
from django.conf import settings
from django.urls import reverse

from backend.signalements.models import Signalement
from backend.unit_tests.factories import SignalementFactory

pytestmark = pytest.mark.django_db(databases=settings.DATABASES.keys())


def test_that_a_signalement_is_listed_in_api_list_endpoint(client):
    SignalementFactory(commune="Test Commune")
    url = reverse("signalement-list")
    response = client.get(url)
    response_data = response.json()
    assert "Test Commune" in str(response_data)


def test_that_a_signalement_is_created_via_api_create_endpoint(client):
    url = reverse("signalement-list")
    data = {
        "commune": "New Test Commune",
        "date_constat": "2025-01-01",
        "heure_constat": "14:30:00",
    }
    assert not Signalement.objects.filter(commune="New Test Commune").exists()
    response = client.post(url, data, content_type="application/json")
    assert Signalement.objects.filter(commune="New Test Commune").exists()
    response_data = response.json()
    assert "New Test Commune" in str(response_data)
    assert "2025-01-01" in str(response_data)
    assert "14:30:00" in str(response_data)


def test_that_a_signalement_is_retrieved_via_api_detail_endpoint(client):
    signalement = SignalementFactory(commune="Retrieve Test Commune")
    url = reverse("signalement-detail", kwargs={"pk": signalement.id})
    response = client.get(url)
    response_data = response.json()
    assert "Retrieve Test Commune" in str(response_data)


def test_that_a_signalement_is_updated_via_api_update_endpoint(client):
    signalement = SignalementFactory(commune="Original Commune")
    url = reverse("signalement-detail", kwargs={"pk": signalement.id})
    data = {
        "commune": "Updated Commune",
        "date_constat": "2025-02-01",
        "heure_constat": "15:45:00",
    }
    response = client.put(url, data, content_type="application/json")
    response_data = response.json()
    assert Signalement.objects.filter(commune="Updated Commune").exists()
    assert "Updated Commune" in str(response_data)
    signalement.refresh_from_db()
    assert signalement.commune == "Updated Commune"
