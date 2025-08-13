import pytest
from django.conf import settings
from django.urls import reverse

from backend.signalements.models import Signalement

pytestmark = pytest.mark.django_db(databases=settings.DATABASES.keys())


def test_signalements_api_loads_correctly(client):
    Signalement.objects.create(
        commune="Test Commune", date_constat="2025-01-01", heure_constat="10:00:00"
    )
    url = reverse("signalement-list")
    response = client.get(url)
    response_data = response.json()
    assert "Test Commune" in str(response_data)
