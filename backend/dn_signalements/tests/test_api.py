import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from backend.dn_signalements.models import DNSignalement
from backend.unit_tests.factories import DNSignalementFactory, UserFactory

pytestmark = pytest.mark.django_db(databases=settings.DATABASES.keys())


def test_that_a_dn_signalement_is_retrieved_via_api_detail_endpoint(client):
    user = UserFactory()
    client.force_login(user)
    signalement = DNSignalementFactory(commune="Retrieve Test Commune")
    url = reverse("dn-signalement-detail", kwargs={"pk": signalement.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "Retrieve Test Commune" in str(response_data)


def test_that_a_dn_signalement_is_updated_via_api_update_endpoint(client):
    user = UserFactory()
    client.force_login(user)
    signalement = DNSignalementFactory(commune="Original Commune")
    url = reverse("dn-signalement-detail", kwargs={"pk": signalement.id})
    data = {
        "commune": "Updated Commune",
        "date_constat": "2025-02-01",
        "heure_constat": "15:45:00",
    }
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert DNSignalement.objects.filter(commune="Updated Commune").exists()
    assert "Updated Commune" in str(response_data)
    signalement.refresh_from_db()
    assert signalement.commune == "Updated Commune"


def test_that_a_dn_signalement_delete_endpoint_is_not_available(client):
    user = UserFactory()
    client.force_login(user)
    signalement = DNSignalementFactory(commune="Delete Test Commune")
    url = reverse("dn-signalement-detail", kwargs={"pk": signalement.id})
    assert DNSignalement.objects.filter(id=signalement.id).exists()
    response = client.delete(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert DNSignalement.objects.filter(id=signalement.id).exists()
