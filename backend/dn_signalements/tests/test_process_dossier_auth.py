from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from backend.dn_signalements.models import DNSignalement

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="password"
    )


@pytest.mark.django_db
@patch("backend.dn_signalements.views.DNGraphQLClient")
def test_process_dossier_success_match_email(mock_client_class, client, user):
    client.force_login(user)

    mock_client = mock_client_class.return_value
    mock_client.get_dossier.return_value = {
        "number": 12345,
        "usager": {"email": "test@example.com"},
        "champs": [],
    }

    url = reverse("signalements-process-dn-dossier")
    data = {"dossier_id": "12345"}

    response = client.post(url, data, content_type="application/json")

    assert response.status_code == status.HTTP_200_OK

    signalement = DNSignalement.objects.get(dn_numero_dossier=12345)
    assert signalement.user == user


@pytest.mark.django_db
@patch("backend.dn_signalements.views.DNGraphQLClient")
def test_process_dossier_fail_mismatch_email(mock_client_class, client, user):
    client.force_login(user)
    mock_client = mock_client_class.return_value
    mock_client.get_dossier.return_value = {
        "number": 12345,
        "usager": {"email": "other@example.com"},
        "champs": [],
    }
    url = reverse("signalements-process-dn-dossier")
    data = {"dossier_id": "12345"}
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not DNSignalement.objects.filter(dn_numero_dossier=12345).exists()


@pytest.mark.django_db
def test_process_dossier_unauthenticated_fails(client):
    url = reverse("signalements-process-dn-dossier")
    response = client.post(url, {"dossier_id": "123"}, content_type="application/json")
    assert (
        response.status_code == status.HTTP_403_FORBIDDEN
    )  # default for anonymous with IsAuthenticated is 403 or 401
