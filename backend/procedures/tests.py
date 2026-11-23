import datetime

import pytest
from django.contrib.admin.sites import site
from django.test import RequestFactory
from django.urls import reverse
from rest_framework import status

from backend.constatations.models import Constatation
from backend.procedures.admin import SuiviProcedureAdmin
from backend.procedures.models import SuiviProcedure
from backend.teams.models import Team
from backend.unit_tests.factories import UserFactory


@pytest.mark.django_db
def test_suivi_procedure_owner_access(client):
    owner = UserFactory()
    client.force_login(owner)
    constatation = Constatation.objects.create(
        user=owner,
        commune="Paris",
    )
    url = reverse("suivi-procedure-detail", args=[constatation.id])
    # 1. Owner GET (should succeed and auto-create the suivi)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["etape_en_cours"] == 1
    suivi = SuiviProcedure.objects.filter(constatation=constatation).first()
    assert suivi is not None
    # 2. Owner PUT (should succeed)
    data = {
        "etape_en_cours": 2,
        "preuves_fournies": True,
        "numero_suivi_lettre": "1A00915820380",
    }
    response = client.put(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    suivi.refresh_from_db()
    assert suivi.etape_en_cours == 2
    assert suivi.preuves_fournies is True
    assert suivi.numero_suivi_lettre == "1A00915820380"


@pytest.mark.django_db
def test_suivi_procedure_non_owner_access_denied(client):
    owner = UserFactory()
    other_user = UserFactory()
    client.force_login(other_user)
    constatation = Constatation.objects.create(
        user=owner,
        commune="Paris",
    )
    url = reverse("suivi-procedure-detail", args=[constatation.id])
    # Non-owner GET (should return 404)
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # Non-owner PUT (should return 404)
    data = {
        "etape_en_cours": 3,
    }
    response = client.put(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_suivi_procedure_anonymous_access_denied(client):
    owner = UserFactory()
    constatation = Constatation.objects.create(
        user=owner,
        commune="Paris",
    )
    url = reverse("suivi-procedure-detail", args=[constatation.id])
    # Anonymous GET (should return 401/403)
    response = client.get(url)
    assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
def test_suivi_procedure_staff_access(client):
    owner = UserFactory()
    staff_user = UserFactory(is_staff=True)
    client.force_login(staff_user)
    constatation = Constatation.objects.create(
        user=owner,
        commune="Paris",
    )
    url = reverse("suivi-procedure-detail", args=[constatation.id])
    # 1. Staff GET (should succeed and see staff fields like notes_traitement)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "notes_traitement" in response.data
    # 2. Staff PUT (should succeed in updating staff fields)
    data = {
        "etape_en_cours": 3,
        "notes_traitement": "Staff note",
    }
    response = client.put(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    suivi = SuiviProcedure.objects.get(constatation=constatation)
    assert suivi.etape_en_cours == 3
    assert suivi.notes_traitement == "Staff note"


def test_suivi_procedure_admin_queryset_optimizations(db):
    owner = UserFactory()
    staff_user = UserFactory(is_staff=True)
    constatation = Constatation.objects.create(
        user=owner,
        commune="Marseille",
        photos=["data:image/jpeg;base64,samplephoto" * 50],
        doc_constat=b"sample_doc",
        lettre_info=b"sample_lettre",
    )
    suivi = constatation.suivi_procedure
    suivi.personne_assignee = staff_user
    suivi.save()
    admin_instance = SuiviProcedureAdmin(SuiviProcedure, site)
    request = RequestFactory().get("/admin/procedures/suiviprocedure/")
    request.user = staff_user
    qs = admin_instance.get_queryset(request)
    fetched_suivi = qs.get(id=suivi.id)
    assert fetched_suivi.constatation.commune == "Marseille"
    assert fetched_suivi.personne_assignee.id == staff_user.id
    deferred = fetched_suivi.constatation.get_deferred_fields()
    assert "doc_constat" in deferred
    assert "lettre_info" in deferred
    assert "photos" in deferred


@pytest.mark.django_db
def test_suivi_procedure_team_sharing_and_traceability(client):
    team_a = Team.objects.create(name="Team Alpha", siret="11111111111111", siren="111111111")
    team_b = Team.objects.create(name="Team Beta", siret="22222222222222", siren="222222222")
    alice = UserFactory(team=team_a)
    bob = UserFactory(team=team_a)
    charlie = UserFactory(team=team_b)

    c_a = Constatation.objects.create(
        user=alice,
        created_by=alice,
        updated_by=alice,
        team=team_a,
        commune="Alpha City",
        is_draft=False,
    )
    url_a = reverse("suivi-procedure-detail", args=[c_a.id])

    # 1. Bob (same team) can access the SuiviProcedure
    client.force_login(bob)
    res_get = client.get(url_a)
    assert res_get.status_code == status.HTTP_200_OK

    # 2. Bob updates the SuiviProcedure:
    # updated_by should be Bob
    res_update = client.patch(
        url_a,
        {"preuves_fournies": True},
        content_type="application/json",
    )
    assert res_update.status_code == status.HTTP_200_OK
    suivi = SuiviProcedure.objects.get(constatation=c_a)
    assert suivi.preuves_fournies is True
    assert suivi.updated_by == bob

    # 3. Charlie (team B) cannot access SuiviProcedure of team A -> 404
    client.force_login(charlie)
    res_denied = client.get(url_a)
    assert res_denied.status_code == status.HTTP_404_NOT_FOUND

    res_patch_denied = client.patch(
        url_a,
        {"preuves_fournies": False},
        content_type="application/json",
    )
    assert res_patch_denied.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_cannot_reassign_suivi_procedure_constatation(client):
    user = UserFactory()
    client.force_login(user)

    c1 = Constatation.objects.create(user=user, commune="City 1")
    c2 = Constatation.objects.create(user=user, commune="City 2")

    url = reverse("suivi-procedure-detail", args=[c1.id])
    res = client.patch(
        url,
        {"constatation": c2.id, "preuves_fournies": True},
        content_type="application/json",
    )
    assert res.status_code == status.HTTP_200_OK
    suivi_c1 = SuiviProcedure.objects.get(constatation=c1)
    assert suivi_c1.constatation == c1
    assert suivi_c1.constatation != c2


@pytest.mark.django_db
def test_suivi_procedure_optimistic_locking(client):
    team = Team.objects.create(name="Equipe Proc", siret="99999999900011", siren="999999999")
    alice = UserFactory(first_name="Alice", last_name="Dubois", team=team)
    bob = UserFactory(first_name="Bob", last_name="Martin", team=team)

    c = Constatation.objects.create(
        user=alice,
        created_by=alice,
        updated_by=alice,
        team=team,
        commune="Rennes",
        is_draft=False,
    )
    url = reverse("suivi-procedure-detail", args=[c.id])

    # Initialize SuiviProcedure
    client.force_login(alice)
    res_init = client.get(url)
    assert res_init.status_code == status.HTTP_200_OK
    suivi = SuiviProcedure.objects.get(constatation=c)

    # 1. Update without last_synced_modified -> HTTP 200
    res = client.patch(url, {"preuves_fournies": True}, content_type="application/json")
    assert res.status_code == status.HTTP_200_OK
    suivi.refresh_from_db()
    assert suivi.preuves_fournies is True
    assert suivi.updated_by == alice

    current_modified = suivi.modified

    # 2. Update with last_synced_modified synchronised -> HTTP 200
    res_sync = client.patch(
        url,
        {
            "identification_reussie": True,
            "last_synced_modified": current_modified.isoformat(),
        },
        content_type="application/json",
    )
    assert res_sync.status_code == status.HTTP_200_OK
    suivi.refresh_from_db()
    assert suivi.identification_reussie is True

    # Bob has an older timestamp (> 1 sec behind server_modified)
    past_timestamp = (suivi.modified - datetime.timedelta(seconds=5)).isoformat()

    # 3. Bob attempts update with older timestamp -> HTTP 409 Conflict
    client.force_login(bob)
    res_conflict = client.patch(
        url,
        {
            "lettre_signe": True,
            "last_synced_modified": past_timestamp,
        },
        content_type="application/json",
    )
    assert res_conflict.status_code == status.HTTP_409_CONFLICT
    data = res_conflict.json()
    assert data["error"] == "CONCURRENT_MODIFICATION"
    assert "Alice Dubois" in data["message"]
    assert data["updated_by"] == "Alice Dubois"
    assert data["server_modified"] == suivi.modified.isoformat()

    suivi.refresh_from_db()
    assert suivi.lettre_signe is False

    # 4. Bob sends update with force=True -> HTTP 200
    res_force = client.patch(
        url,
        {
            "lettre_signe": True,
            "last_synced_modified": past_timestamp,
            "force": True,
        },
        content_type="application/json",
    )
    assert res_force.status_code == status.HTTP_200_OK
    suivi.refresh_from_db()
    assert suivi.lettre_signe is True
    assert suivi.updated_by == bob
