import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db(databases=settings.DATABASES.keys())


@pytest.mark.skip(reason="Skipped to avoid triggering API call")
def test_process_dossier_returns_success_with_valid_dossier_id(client):
    url = reverse("signalements-process-dn-dossier")
    data = {"dossier_id": 12345}
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "dossier_id" in response_data
    assert response_data["dossier_id"] == 12345


def test_process_dossier_returns_error_when_dossier_id_is_missing(client):
    url = reverse("signalements-process-dn-dossier")
    data = {}
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_data = response.json()
    assert "error" in response_data


def test_process_dossier_returns_error_when_dossier_id_is_none(client):
    url = reverse("signalements-process-dn-dossier")
    data = {"dossier_id": None}
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_data = response.json()
    assert "error" in response_data


def test_process_dossier_returns_no_procedure_when_date_constat_missing(client, mocker):
    """Test that a dossier without date_constat is not processed (no signalement)."""
    url = reverse("signalements-process-dn-dossier")
    data = {"dossier_id": 12345}
    # Mock DN client to return a dossier without date_constat
    mock_dossier = {
        "champs": [],  # No DATE_CONSTAT_CHAMP_ID in champs
        "usager": {"email": "test@example.com"},
        "dateDepot": "2026-01-01T10:00:00Z",
    }
    mocker.patch("backend.dn.client.DNGraphQLClient.get_dossier", return_value=mock_dossier)
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["created"] is False
    assert response_data["reason"] == "no_procedure_or_missing_info"
    assert "dn_date_creation" in response_data


def test_process_dossier_returns_error_on_permission_issue(client, mocker):
    """Test returning a clean error message when permission is denied."""
    url = reverse("signalements-process-dn-dossier")
    data = {"dossier_id": 12345}
    # Mock DN client to raise ValueError with permission message
    mocker.patch(
        "backend.dn.client.DNGraphQLClient.get_dossier",
        side_effect=ValueError(
            "GraphQL errors: An object of type Dossier was hidden due to permissions"
        ),
    )
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_data = response.json()
    assert "error" in response_data
