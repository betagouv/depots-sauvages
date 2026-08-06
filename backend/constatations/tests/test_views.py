import pytest
from django.urls import reverse
from rest_framework import status

from backend.activity_logs.models import ActivityLog
from backend.constatations.models import Constatation
from backend.unit_tests.factories import UserFactory


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_create_constatation_authenticated(client):
    user = UserFactory()
    client.force_login(user)
    url = reverse("constatation-list")
    data = {
        "commune": "Paris",
        "auteur_identifie": True,
    }
    response = client.post(url, data, format="json")
    # Let's check the response status and the database
    assert response.status_code == status.HTTP_201_CREATED
    constatation = Constatation.objects.first()
    assert constatation is not None
    assert constatation.user == user
    assert constatation.commune == "Paris"
    log = ActivityLog.objects.get(action="constatation_demarree")
    assert log.constatation_id == constatation.id
    assert log.suivi_procedure_id == constatation.suivi_procedure.id


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_create_and_complete_draft_constatation(client):
    user = UserFactory()
    client.force_login(user)
    url = reverse("constatation-list")
    
    # 1. Autosave draft (partial payload)
    draft_data = {
        "commune": "Marseille",
        "is_draft": True,
    }
    res_draft = client.post(url, draft_data, format="json")
    assert res_draft.status_code == status.HTTP_201_CREATED
    constatation = Constatation.objects.get(id=res_draft.data["id"])
    assert constatation.is_draft is True
    assert constatation.doc_constat_should_generate is False

    # 2. Final submission (is_draft=False)
    detail_url = reverse("constatation-detail", args=[constatation.id])
    final_data = {
        "commune": "Marseille",
        "is_draft": False,
        "auteur_identifie": False,
    }
    res_final = client.put(detail_url, final_data, content_type="application/json")
    assert res_final.status_code == status.HTTP_200_OK
    constatation.refresh_from_db()
    assert constatation.is_draft is False
    assert constatation.doc_constat is not None
    assert ActivityLog.objects.filter(action="constatation_terminee", constatation_id=constatation.id).exists()



@pytest.mark.django_db(databases=["default", "stats_db"])
def test_create_constatation_anonymous(client):
    url = reverse("constatation-list")
    data = {
        "commune": "Paris",
        "auteur_identifie": True,
    }
    response = client.post(url, data, format="json")
    # Unauthenticated requests should be rejected
    assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    assert Constatation.objects.count() == 0


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_update_constatation_prejudice(client):
    user = UserFactory()
    client.force_login(user)
    # Create initial constatation
    constatation = Constatation.objects.create(
        user=user,
        commune="Paris",
        plainte_etat="Déposée",
        prejudice_montant_connu=False,
        prejudice_nombre_personnes=5,
        prejudice_nombre_heures=2,
    )
    url = reverse("constatation-detail", args=[constatation.id])
    # Update to prejudice_montant_connu = True
    data = {
        "commune": "Paris",
        "plainte_etat": "Déposée",
        "prejudice_montant_connu": True,
        "prejudice_montant": 500,
        "prejudice_nombre_personnes": None,
        "prejudice_nombre_heures": None,
        "prejudice_nombre_vehicules": None,
        "prejudice_kilometrage": None,
        "prejudice_autres_couts": None,
    }
    response = client.put(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    constatation.refresh_from_db()
    assert constatation.prejudice_montant_connu is True
    assert constatation.prejudice_montant == 500
    assert constatation.prejudice_nombre_personnes is None


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_download_document_permissions(client):
    owner = UserFactory(is_staff=False)
    other_user = UserFactory(is_staff=False)
    staff_user = UserFactory(is_staff=True)

    c = Constatation.objects.create(
        user=owner,
        commune="Paris",
        doc_constat=b"dummy_content",
    )

    url = reverse(
        "constatation-document-download",
        kwargs={"pk": c.id, "doc_type": "doc-constat"},
    )

    # 1. Owner download (should succeed)
    client.force_login(owner)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert b"".join(response.streaming_content) == b"dummy_content"

    # 2. Other user download (should return 404)
    client.force_login(other_user)
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # 3. Staff user download (should succeed)
    client.force_login(staff_user)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert b"".join(response.streaming_content) == b"dummy_content"

    # 4. Verify ActivityLogs for download events (owner and staff generated 2 logs across 2 distinct sessions)
    logs = ActivityLog.objects.using("stats_db").filter(
        action="doc_constat_telecharge", constatation_id=c.id
    )
    assert logs.count() == 2
