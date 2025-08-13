import pytest
from django.conf import settings
from django.urls import reverse

from backend.unit_tests.factories import SignalementFactory

pytestmark = pytest.mark.django_db(databases=settings.DATABASES.keys())


def test_signalements_api_loads_correctly(client):
    SignalementFactory(commune="Test Commune")
    url = reverse("signalement-list")
    response = client.get(url)
    response_data = response.json()
    assert "Test Commune" in str(response_data)
