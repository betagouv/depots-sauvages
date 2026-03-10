from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status

from backend.unit_tests.factories import UserFactory


@pytest.mark.django_db
class TestSyncAPI:
    def test_sync_endpoint_requires_auth(self, client):
        url = reverse("dossiers-sync")
        response = client.post(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_sync_endpoint_triggers_task(self, client):
        user = UserFactory()
        client.force_login(user)
        url = reverse("dossiers-sync")
        # Using create=True because it's imported locally in the view method
        with patch("backend.dn_signalements.views.sync_user_dossiers", create=True) as mock_task:
            response = client.post(url)
            assert response.status_code == status.HTTP_202_ACCEPTED
            assert response.data["status"] == "sync_triggered"
            mock_task.enqueue.assert_called_once_with(user.id)
