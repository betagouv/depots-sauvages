import pytest
from django.conf import settings
from django.urls import reverse

from backend.signalements.signals import generate_document
from backend.unit_tests.factories import SignalementFactory

pytestmark = pytest.mark.django_db(databases=settings.DATABASES.keys())


def test_that_doc_constat_download_works(client):
    signalement = SignalementFactory(commune="Test Commune")
    signalement.doc_constat = b"fake document content"
    signalement.save()
    url = reverse(
        "signalement-document-download", kwargs={"pk": signalement.id, "doc_type": "doc-constat"}
    )
    response = client.get(url)
    assert response.status_code == 200
    assert response["Content-Type"] == "application/vnd.oasis.opendocument.text"
    expected_filename = f"rapport-constatation-{signalement.id}-{signalement.commune}.odt"
    assert response["Content-Disposition"] == f'attachment; filename="{expected_filename}"'


def test_that_doc_constat_generation_works(client):
    signalement = SignalementFactory(commune="Test Commune")
    generate_document(signalement.id, doc_base_name="doc_constat")
    signalement.refresh_from_db()
    assert signalement.doc_constat is not None
    assert signalement.doc_constat_generated_at is not None


def test_that_lettre_info_download_works(client):
    signalement = SignalementFactory(commune="Test Commune")
    signalement.lettre_info = b"fake letter content"
    signalement.save()
    url = reverse(
        "signalement-document-download", kwargs={"pk": signalement.id, "doc_type": "lettre-info"}
    )
    response = client.get(url)
    assert response.status_code == 200
    assert response["Content-Type"] == "application/vnd.oasis.opendocument.text"
    expected_filename = f"lettre-info-{signalement.id}-{signalement.commune}.odt"
    assert response["Content-Disposition"] == f'attachment; filename="{expected_filename}"'


def test_that_lettre_info_generation_works(client):
    signalement = SignalementFactory(commune="Test Commune")
    generate_document(signalement.id, doc_base_name="lettre_info")
    signalement.refresh_from_db()
    assert signalement.lettre_info is not None
    assert signalement.lettre_info_generated_at is not None
