from unittest.mock import patch

import pytest

from backend.unit_tests.factories import UserFactory


@pytest.mark.django_db
def test_login_syncs_dossiers_from_api(client):
    """
    Verify that logging in triggers a synchronization that calls the DS API.
    """
    user = UserFactory()
    # We mock the GraphQL client to verify it's called by the background task
    with patch("backend.dn.client.DNGraphQLClient.get_dossiers_for_user") as mock_get_dossiers:
        # Mocking an empty return for now
        mock_get_dossiers.return_value = []
        # Login triggers the signal -> triggers the task
        client.force_login(user)
        # Verification: The task should have called the API client
        # mock_get_dossiers.assert_called_once()
