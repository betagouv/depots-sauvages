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
    response = client.post(url, data)
    assert Signalement.objects.filter(commune="New Test Commune").exists()
    response_data = response.json()
    assert "New Test Commune" in str(response_data)
    assert "2025-01-01" in str(response_data)
    assert "14:30:00" in str(response_data)
