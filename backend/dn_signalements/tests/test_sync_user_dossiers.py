from unittest.mock import patch

import pytest

from backend.dn_signalements.models import UserDossier
from backend.unit_tests.factories import UserFactory


@pytest.mark.django_db
def test_login_syncs_dossiers_from_api(client):
    """
    Verify that logging in triggers a synchronization that calls the DS API.
    """
    user = UserFactory()
    # We mock the GraphQL client to verify it's called by the background task
    with patch("backend.dn.client.DNGraphQLClient.get_dossiers_for_user") as mock_get_dossiers:
        # Mocking a return value with one dossier
        mock_get_dossiers.return_value = [
            {
                "number": 12345,
                "dateDepot": "2024-01-01T12:00:00Z",
                "dateDerniereModification": "2024-01-02T12:00:00Z",
                "champs": [],
            }
        ]
        # Login triggers the signal -> triggers the task
        client.force_login(user)
        # Verification: The task should have called the API client
        mock_get_dossiers.assert_called_once()
        # Verification: UserDossier should be created in DB
        assert UserDossier.objects.filter(user=user, numero_dossier=12345).exists()
        dossier = UserDossier.objects.get(numero_dossier=12345)
        assert dossier.numero_dossier == 12345
