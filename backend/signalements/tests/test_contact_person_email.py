import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from backend.unit_tests.factories import SignalementFactory

pytestmark = pytest.mark.django_db(databases=settings.DATABASES.keys())


def test_that_send_contact_email_ok_when_contact_email_exists(client):
    signalement = SignalementFactory(contact_email="test@example.com")
    url = reverse("signalement-send-contact-email", kwargs={"pk": signalement.id})
    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK


def test_that_send_contact_email_fails_when_no_contact_email(client):
    signalement = SignalementFactory(contact_email="")
    url = reverse("signalement-send-contact-email", kwargs={"pk": signalement.id})
    response = client.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_that_send_contact_email_fails_for_nonexistent_signalement(client):
    url = reverse("signalement-send-contact-email", kwargs={"pk": 99999})
    response = client.post(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
