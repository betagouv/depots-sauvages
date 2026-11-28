import datetime

import pytest
from django.urls import reverse
from rest_framework import status

from backend.activity_logs.models import ActivityLog
from backend.constatations.models import Constatation
from backend.constatations.views import get_user_constatations_queryset
from backend.teams.models import Team
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
    assert constatation.created_by == user
    assert constatation.updated_by == user
    assert constatation.team is None
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

    # 1b. Autosave update (PUT/PATCH on draft to update commune and constatant_role)
    detail_url = reverse("constatation-detail", args=[constatation.id])
    autosave_data = {
        "commune": "Nice",
        "constatant_role": "Maire",
        "is_draft": True,
    }
    res_autosave = client.put(detail_url, autosave_data, content_type="application/json")
    assert res_autosave.status_code == status.HTTP_200_OK
    log = ActivityLog.objects.get(action="constatation_demarree", constatation_id=constatation.id)
    assert log.data["commune"] == "Nice"
    assert log.data["constatant_role"] == "Maire"

    # 2. Final submission (is_draft=False)
    final_data = {
        "commune": "Nice",
        "constatant_role": "Maire",
        "is_draft": False,
        "auteur_identifie": False,
    }
    res_final = client.put(detail_url, final_data, content_type="application/json")
    assert res_final.status_code == status.HTTP_200_OK
    constatation.refresh_from_db()
    assert constatation.is_draft is False
    assert constatation.doc_constat is not None
    assert ActivityLog.objects.filter(
        action="constatation_terminee", constatation_id=constatation.id
    ).exists()


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

    # 4. Verify ActivityLogs for download events
    # (owner and staff generated 2 logs across 2 distinct sessions)
    logs = ActivityLog.objects.using("stats_db").filter(
        action="doc_constat_telecharge", constatation_id=c.id
    )
    assert logs.count() == 2


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_list_constatations_returns_lightweight_payload(client):
    user = UserFactory()
    client.force_login(user)
    c = Constatation.objects.create(
        user=user,
        commune="Lyon",
        localisation_depot="Rue de la République",
        photos=["data:image/jpeg;base64,largephotodata" * 100],
        doc_constat=b"binary_odt_content",
        lettre_info=b"binary_lettre_content",
    )
    url = reverse("constatation-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    item = data[0]
    assert item["id"] == c.id
    assert item["commune"] == "Lyon"
    assert item["localisation_depot"] == "Rue de la République"
    assert "suivi_procedure" in item
    # Verify that heavy fields like photos are not in the list response
    assert "photos" not in item
    assert "doc_constat" not in item
    assert "lettre_info" not in item


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_list_constatations_includes_auteur_and_suivi_resume(client):
    user = UserFactory()
    client.force_login(user)
    c = Constatation.objects.create(
        user=user,
        commune="Reignier-Ésery",
        auteur_identifie=True,
        auteur_nom="Dupont",
        auteur_prenom="Marc",
        is_draft=False,
    )
    suivi = c.suivi_procedure
    suivi.lettre_envoyee = True
    suivi.lettre_envoyee_date = "2026-10-01"
    suivi.ar_presentation_date = "2026-10-03"
    suivi.save()

    response = client.get(reverse("constatation-list"))
    assert response.status_code == status.HTTP_200_OK
    item = response.json()[0]
    assert item["auteur_nom"] == "Dupont"
    assert item["auteur_prenom"] == "Marc"
    resume = item["suivi_procedure"]
    assert resume["lettre_envoyee"] is True
    assert resume["lettre_envoyee_date"] == "2026-10-01"
    assert resume["ar_presentation_date"] == "2026-10-03"
    assert resume["dossier_archive"] is False
    # Internal notes and processing notes are not included in the list view
    assert "observations_internes" not in resume
    assert "notes_traitement" not in resume


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_constatation_photos_max_length_validation(client):
    user = UserFactory()
    client.force_login(user)
    payload = {
        "commune": "Lyon",
        "photos": [f"data:image/jpeg;base64,photo{i}" for i in range(11)],
    }
    response = client.post(
        reverse("constatation-list"), data=payload, content_type="application/json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "photos" in response.json()


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_team_member_sees_and_updates_team_constatations(client):
    team_a = Team.objects.create(name="Commune A", siret="11111111111111", siren="111111111")
    alice = UserFactory(team=team_a)
    bob = UserFactory(team=team_a)

    # Alice creates a draft constatation
    client.force_login(alice)
    create_res = client.post(
        reverse("constatation-list"),
        {"commune": "Village A", "is_draft": True},
        format="json",
    )
    assert create_res.status_code == status.HTTP_201_CREATED
    constat_id = create_res.data["id"]

    constat = Constatation.objects.get(id=constat_id)
    assert constat.team == team_a
    assert constat.created_by == alice
    assert constat.updated_by == alice

    # Drafts are private to their creator: Bob does NOT see Alice's draft
    client.force_login(bob)
    list_res_bob = client.get(reverse("constatation-list"))
    assert list_res_bob.status_code == status.HTTP_200_OK
    assert len(list_res_bob.json()) == 0

    # Alice finalizes the constatation (is_draft = False)
    client.force_login(alice)
    finalize_res = client.patch(
        reverse("constatation-detail", args=[constat_id]),
        {"is_draft": False},
        content_type="application/json",
    )
    assert finalize_res.status_code == status.HTTP_200_OK

    # Now Bob sees the validated constatation in the team list
    client.force_login(bob)
    list_res_bob_after = client.get(reverse("constatation-list"))
    assert list_res_bob_after.status_code == status.HTTP_200_OK
    assert len(list_res_bob_after.json()) == 1
    assert list_res_bob_after.json()[0]["id"] == constat_id

    # Bob can retrieve the detail
    detail_res = client.get(reverse("constatation-detail", args=[constat_id]))
    assert detail_res.status_code == status.HTTP_200_OK

    # Bob updates the constatation
    update_res = client.patch(
        reverse("constatation-detail", args=[constat_id]),
        {"commune": "Village A Modifié"},
        content_type="application/json",
    )
    assert update_res.status_code == status.HTTP_200_OK
    constat.refresh_from_db()
    assert constat.commune == "Village A Modifié"
    assert constat.created_by == alice
    assert constat.updated_by == bob


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_team_isolation_cross_teams_denied(client):
    team_a = Team.objects.create(name="Commune A", siret="11111111111111", siren="111111111")
    team_b = Team.objects.create(name="Commune B", siret="22222222222222", siren="222222222")
    agent_a = UserFactory(team=team_a)
    agent_b = UserFactory(team=team_b)

    constat_b = Constatation.objects.create(
        user=agent_b,
        created_by=agent_b,
        updated_by=agent_b,
        team=team_b,
        commune="Commune B City",
        doc_constat=b"odt_doc_b",
    )

    client.force_login(agent_a)

    # agent_a lists constatations -> empty
    list_res = client.get(reverse("constatation-list"))
    assert list_res.status_code == status.HTTP_200_OK
    assert len(list_res.json()) == 0

    # agent_a tries to retrieve constat_b -> 404
    detail_res = client.get(reverse("constatation-detail", args=[constat_b.id]))
    assert detail_res.status_code == status.HTTP_404_NOT_FOUND

    # agent_a tries to update constat_b -> 404
    update_res = client.patch(
        reverse("constatation-detail", args=[constat_b.id]),
        {"commune": "Hacked"},
        content_type="application/json",
    )
    assert update_res.status_code == status.HTTP_404_NOT_FOUND

    # agent_a tries to download document of constat_b -> 404
    download_url = reverse(
        "constatation-document-download",
        kwargs={"pk": constat_b.id, "doc_type": "doc-constat"},
    )
    download_res = client.get(download_url)
    assert download_res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_user_without_team_isolation(client):
    solo_user = UserFactory()  # team is None
    other_user = UserFactory()  # team is None

    constat_other = Constatation.objects.create(
        user=other_user,
        created_by=other_user,
        updated_by=other_user,
        team=None,
        commune="Other Solo City",
    )
    constat_solo = Constatation.objects.create(
        user=solo_user,
        created_by=solo_user,
        updated_by=solo_user,
        team=None,
        commune="My Solo City",
    )

    client.force_login(solo_user)
    list_res = client.get(reverse("constatation-list"))
    assert list_res.status_code == status.HTTP_200_OK
    ids = [item["id"] for item in list_res.json()]
    assert constat_solo.id in ids
    assert constat_other.id not in ids

    # Cannot view other solo constat
    detail_res = client.get(reverse("constatation-detail", args=[constat_other.id]))
    assert detail_res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_staff_user_only_sees_own_or_team_constatations(client):
    team_a = Team.objects.create(name="Commune A", siret="11111111111111", siren="111111111")
    team_b = Team.objects.create(name="Commune B", siret="22222222222222", siren="222222222")
    user_a = UserFactory(team=team_a)
    user_b = UserFactory(team=team_b)
    user_solo = UserFactory()

    c_a = Constatation.objects.create(user=user_a, created_by=user_a, team=team_a, commune="A")
    c_b = Constatation.objects.create(user=user_b, created_by=user_b, team=team_b, commune="B")
    c_solo = Constatation.objects.create(
        user=user_solo, created_by=user_solo, team=None, commune="Solo"
    )

    staff = UserFactory(is_staff=True)
    c_staff = Constatation.objects.create(
        user=staff, created_by=staff, team=None, commune="StaffOwn"
    )
    client.force_login(staff)

    list_res = client.get(reverse("constatation-list"))
    assert list_res.status_code == status.HTTP_200_OK
    ids = [item["id"] for item in list_res.json()]
    assert ids == [c_staff.id]
    assert c_a.id not in ids
    assert c_b.id not in ids
    assert c_solo.id not in ids


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_user_cannot_spoof_constatation_owner(client):
    owner = UserFactory()
    attacker = UserFactory()
    client.force_login(owner)

    constat = Constatation.objects.create(
        user=owner,
        created_by=owner,
        updated_by=owner,
        commune="Origine",
    )
    detail_url = reverse("constatation-detail", args=[constat.id])

    # Attempt to change user/owner via PATCH payload
    response = client.patch(
        detail_url,
        {"user": attacker.id, "commune": "Modifiee"},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_200_OK
    constat.refresh_from_db()
    assert constat.user == owner
    assert constat.user != attacker
    assert constat.commune == "Modifiee"


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_inactive_user_access_denied(client):
    user = UserFactory(is_active=False)
    Constatation.objects.create(
        user=user,
        created_by=user,
        commune="Ghost Town",
    )
    # Queryset returns empty for inactive user
    assert get_user_constatations_queryset(user).count() == 0

    # DRF view returns 401/403 for inactive user
    client.force_login(user)
    response = client.get(reverse("constatation-list"))
    assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_constatation_optimistic_locking(client):
    team = Team.objects.create(name="Equipe Test", siret="12345678901234", siren="123456789")
    alice = UserFactory(first_name="Alice", last_name="Smith", team=team)
    bob = UserFactory(first_name="Bob", last_name="Jones", team=team)

    constat = Constatation.objects.create(
        user=alice,
        created_by=alice,
        updated_by=alice,
        team=team,
        commune="Paris",
        is_draft=False,
    )
    detail_url = reverse("constatation-detail", args=[constat.id])

    # 1. Update without last_synced_modified -> HTTP 200 (backward compatibility)
    client.force_login(alice)
    res = client.patch(detail_url, {"commune": "Lyon"}, content_type="application/json")
    assert res.status_code == status.HTTP_200_OK
    constat.refresh_from_db()
    assert constat.commune == "Lyon"
    assert constat.updated_by == alice

    current_modified = constat.modified

    # 2. Update with last_synced_modified synchronised (within tolerance) -> HTTP 200
    res_sync = client.patch(
        detail_url,
        {"commune": "Marseille", "last_synced_modified": current_modified.isoformat()},
        content_type="application/json",
    )
    assert res_sync.status_code == status.HTTP_200_OK
    constat.refresh_from_db()
    assert constat.commune == "Marseille"

    # Bob simulates having an older timestamp (> 1 sec behind server_modified)
    past_timestamp = (constat.modified - datetime.timedelta(seconds=5)).isoformat()

    # 3. Bob sends update with older last_synced_modified -> HTTP 409 Conflict
    client.force_login(bob)
    res_conflict = client.patch(
        detail_url,
        {"commune": "Bordeaux", "last_synced_modified": past_timestamp},
        content_type="application/json",
    )
    assert res_conflict.status_code == status.HTTP_409_CONFLICT
    data = res_conflict.json()
    assert data["error"] == "CONCURRENT_MODIFICATION"
    assert "Alice Smith" in data["message"]
    assert data["updated_by"] == "Alice Smith"
    assert data["server_modified"] == constat.modified.isoformat()

    # Verify database was NOT changed
    constat.refresh_from_db()
    assert constat.commune == "Marseille"

    # 4. Bob sends update with force=True -> HTTP 200 (force overwrite)
    res_force = client.patch(
        detail_url,
        {
            "commune": "Bordeaux",
            "last_synced_modified": past_timestamp,
            "force": True,
        },
        content_type="application/json",
    )
    assert res_force.status_code == status.HTTP_200_OK
    constat.refresh_from_db()
    assert constat.commune == "Bordeaux"
    assert constat.updated_by == bob

    # 5. Robustness & Security: invalid or malicious last_synced_modified
    # - non-string payload (e.g. dict or list) -> ignored safely, HTTP 200
    res_malicious_type = client.patch(
        detail_url,
        {"commune": "Nice", "last_synced_modified": {"evil": "data"}},
        content_type="application/json",
    )
    assert res_malicious_type.status_code == status.HTTP_200_OK

    # - excessively long string (DoS prevention) -> ignored safely, HTTP 200
    res_dos_len = client.patch(
        detail_url,
        {"commune": "Nice", "last_synced_modified": "2026-01-01" * 50},
        content_type="application/json",
    )
    assert res_dos_len.status_code == status.HTTP_200_OK

    # - invalid datetime format -> ignored safely, HTTP 200
    res_invalid_date = client.patch(
        detail_url,
        {"commune": "Nice", "last_synced_modified": "not-a-date"},
        content_type="application/json",
    )
    assert res_invalid_date.status_code == status.HTTP_200_OK

    # - naive datetime string (no timezone offset) -> handled without crash, triggers 409
    naive_past = (constat.modified - datetime.timedelta(seconds=10)).strftime("%Y-%m-%dT%H:%M:%S")
    res_naive = client.patch(
        detail_url,
        {"commune": "Toulouse", "last_synced_modified": naive_past},
        content_type="application/json",
    )
    assert res_naive.status_code == status.HTTP_409_CONFLICT
