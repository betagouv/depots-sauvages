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
def test_proconnect_access_request_requires_session():
    client = APIClient()
    url = reverse("proconnect-demander-acces")
    response = client.post(url, {"message": "Je demande un accès"}, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_proconnect_access_request_uses_session_data_and_ignores_forged_payload(settings):
    settings.ADMIN_EMAIL = "admin@depots-sauvages.beta.gouv.fr"
    client = APIClient()
    url = reverse("proconnect-demander-acces")
    session = client.session
    session["proconnect_rejected_info"] = {
        "siret": "12345678900012",
        "siren": "123456789",
        "organization_label": "Académie de Paris",
        "email": "agent@ac-paris.fr",
        "name": "Jean Dupont",
    }
    session.save()
    forged_payload = {
        "siret": "99999999999999",
        "siren": "999999999",
        "organization_label": "Mairie Pirate",
        "email": "hacker@evil.com",
        "name": "Evil Actor",
        "message": "Nous souhaitons déclarer des dépôts sauvages aux abords des lycées.",
    }
    response = client.post(url, forged_payload, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True
    assert len(mail.outbox) == 1
    sent_email = mail.outbox[0]
    assert "Demande d'accès ProConnect" in sent_email.subject
    assert "Académie de Paris" in sent_email.subject
    assert "Mairie Pirate" not in sent_email.subject
    assert sent_email.to == ["admin@depots-sauvages.beta.gouv.fr"]
    assert "123456789" in sent_email.body
    assert "999999999" not in sent_email.body
    assert "Jean Dupont" in sent_email.body
    assert "Evil Actor" not in sent_email.body
    assert "agent@ac-paris.fr" in sent_email.body
    assert "hacker@evil.com" not in sent_email.body
    assert "Académie de Paris" in sent_email.body
    assert "Nous souhaitons déclarer des dépôts sauvages" in sent_email.body
    assert "proconnect/proconnectaccessconfig/" in sent_email.body
