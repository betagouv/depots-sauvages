import pytest
from django.conf import settings
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_proconnect_rejected_info_endpoint():
    client = APIClient()
    url = reverse("proconnect-rejected-info")
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    session = client.session
    session["proconnect_rejected_info"] = {
        "siret": "12345678900012",
        "siren": "123456789",
        "organization_label": "Académie de Paris",
        "email": "agent@ac-paris.fr",
        "name": "Jean Dupont",
    }
    session.save()
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["siren"] == "123456789"
    assert data["organization_label"] == "Académie de Paris"
    assert data["email"] == "agent@ac-paris.fr"
    assert data["name"] == "Jean Dupont"


@pytest.mark.django_db
def test_proconnect_access_request_endpoint_validation():
    client = APIClient()
    url = reverse("proconnect-demander-acces")
    response = client.post(url, {}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response = client.post(url, {"email": "agent@ac-paris.fr"}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_proconnect_access_request_endpoint_success(settings):
    settings.ADMIN_EMAIL = "admin@depots-sauvages.beta.gouv.fr"
    client = APIClient()
    url = reverse("proconnect-demander-acces")
    payload = {
        "siret": "12345678900012",
        "siren": "123456789",
        "organization_label": "Académie de Paris",
        "email": "agent@ac-paris.fr",
        "name": "Jean Dupont",
        "message": "Nous souhaitons déclarer des dépôts sauvages aux abords des lycées.",
    }
    response = client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True
    assert len(mail.outbox) == 1
    sent_email = mail.outbox[0]
    assert "Demande d'accès ProConnect" in sent_email.subject
    assert "Académie de Paris" in sent_email.subject
    assert sent_email.to == ["admin@depots-sauvages.beta.gouv.fr"]
    assert "123456789" in sent_email.body
    assert "Jean Dupont" in sent_email.body
    assert "agent@ac-paris.fr" in sent_email.body
    assert "Académie de Paris" in sent_email.body
    assert "Nous souhaitons déclarer des dépôts sauvages" in sent_email.body
    assert "proconnect/proconnectaccessconfig/" in sent_email.body
