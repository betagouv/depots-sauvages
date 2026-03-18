from unittest.mock import patch

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from backend.unit_tests.factories import UserFactory

pytestmark = pytest.mark.django_db(databases=settings.DATABASES.keys())


@pytest.mark.skip(reason="Skipped to avoid triggering API call")
def test_process_dossier_returns_success_with_valid_dossier_id(client):
    user = UserFactory()
    client.force_login(user)
    url = reverse("signalements-process-dn-dossier")
    data = {"dossier_id": 12345}
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "dossier_id" in response_data
    assert response_data["dossier_id"] == 12345


def test_process_dossier_returns_error_when_dossier_id_is_missing(client):
    user = UserFactory()
    client.force_login(user)
    url = reverse("signalements-process-dn-dossier")
    data = {}
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_data = response.json()
    assert "error" in response_data


def test_process_dossier_returns_error_when_dossier_id_is_none(client):
    user = UserFactory()
    client.force_login(user)
    url = reverse("signalements-process-dn-dossier")
    data = {"dossier_id": None}
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_data = response.json()
    assert "error" in response_data


def test_process_dossier_returns_no_procedure_when_date_constat_missing(client):
    """Test that a dossier without date_constat is not processed (no signalement)."""
    user = UserFactory()
    client.force_login(user)
    url = reverse("signalements-process-dn-dossier")
    data = {"dossier_id": 12345}
    # Mock DN client to return a dossier without date_constat
    mock_dossier = {
        "champs": [],  # No DATE_CONSTAT_CHAMP_ID in champs
        "usager": {"email": "test@example.com"},
        "dateDepot": "2026-01-01T10:00:00Z",
    }
    with patch("backend.dn.client.DNGraphQLClient.get_dossier", return_value=mock_dossier):
        response = client.post(url, data, content_type="application/json")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["created"] is False
        assert response_data["reason"] == "no_procedure_or_missing_info"
        assert "dn_date_creation" in response_data


def test_process_dossier_returns_error_on_permission_issue(client):
    """Test returning a clean error message when permission is denied."""
    user = UserFactory()
    client.force_login(user)
    url = reverse("signalements-process-dn-dossier")
    data = {"dossier_id": 12345}
    # Mock DN client to raise ValueError with permission message
    with patch(
        "backend.dn.client.DNGraphQLClient.get_dossier",
        side_effect=ValueError(
            "GraphQL errors: An object of type Dossier was hidden due to permissions"
        ),
    ):
        response = client.post(url, data, content_type="application/json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert "error" in response_data


def test_process_dossier_returns_full_date_constat(client):
    """Test that date_constat in response is a full ISO datetime string."""
    user = UserFactory()
    client.force_login(user)
    url = reverse("signalements-process-dn-dossier")
    data = {"dossier_id": 12345}
    # Mock DN client to return a dossier with date_constat
    mock_dossier = {
        "champs": [
            {
                "id": "Q2hhbXAtNTYxNzM2MQ==",
                "datetime": "2026-03-11T12:16:00Z",
                "__typename": "DatetimeChamp",
            }
        ],
        "usager": {"email": "test@example.com"},
        "dateDepot": "2026-01-01T10:00:00Z",
    }
    with patch("backend.dn.client.DNGraphQLClient.get_dossier", return_value=mock_dossier):
        response = client.post(url, data, content_type="application/json")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["created"] is True
        # The date_constat should be a full ISO string (including time)
        # Note: DRF serializes datetime as "YYYY-MM-DDTHH:MM:SSZ" (UTC)
        assert response_data["date_constat"].startswith("2026-03-11T12:16:00")
