import pytest
from django.urls import reverse
from rest_framework import status

from backend.constatations.models import Constatation
from backend.unit_tests.factories import UserFactory


@pytest.mark.django_db
def test_backoffice_procedures_anonymous(client):
    url = reverse("backoffice-procedures-list")
    response = client.get(url)
    assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
def test_backoffice_procedures_non_staff(client):
    user = UserFactory(is_staff=False)
    client.force_login(user)
    url = reverse("backoffice-procedures-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_backoffice_procedures_staff(client):
    staff_user = UserFactory(is_staff=True)
    client.force_login(staff_user)

    # Create a constatation with a suivi_procedure
    c1 = Constatation.objects.create(
        user=staff_user,
        commune="Montmédy",
        date_constat="2026-06-27",
        constatant_role="Secrétaire de mairie",
        volume_depot="3 m³",
        nature_terrain=["Terrain public"],
        ceci_est_un_test=False,
    )
    sp1 = c1.suivi_procedure
    sp1.etape_en_cours = 1
    sp1.preuves_fournies = False
    sp1.constatation_signee = False
    sp1.lettre_signe = False
    sp1.identification_reussie = None
    sp1.observations_internes = "Some notes"
    sp1.save()

    # Create a constatation without a suivi_procedure (to test default fallback)
    c2 = Constatation.objects.create(
        user=staff_user,
        commune="Fécamp",
        date_constat="2026-05-27",
        constatant_role="Gendarme",
        volume_depot="10 m³",
        nature_terrain=["Terrain privé"],
        ceci_est_un_test=False,
    )


@pytest.mark.django_db
def test_backoffice_dashboard_stats(client):
    staff_user = UserFactory(is_staff=True)
    client.force_login(staff_user)

    Constatation.objects.create(
        user=staff_user,
        commune="Montmédy",
        ceci_est_un_test=False,
        auteur_identifie=True,
    )
    Constatation.objects.create(
        user=staff_user,
        commune="Fécamp",
        ceci_est_un_test=True,
        auteur_identifie=False,
    )

    url = reverse("backoffice-dashboard-stats-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "generalStats" in data
    assert data["generalStats"]["real"] == 1
    assert data["generalStats"]["test"] == 1
    assert data["generalStats"]["authorIdentified"] == 1
    assert "steps" in data
    assert "byStatus" in data

    url = reverse("backoffice-procedures-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    res = response.json()
    assert "results" in res
    data = res["results"]
    assert len(data) == 2

    # Verify first (c2 is newer / higher ID, so first in order-by "-id")
    assert data[0]["id"] == c2.id
    assert data[0]["commune"] == "Fécamp"
    assert data[0]["user_email"] == staff_user.email
    assert data[0]["suivi_procedure"]["etape_en_cours"] == 1
    assert data[0]["suivi_procedure"]["personne_assignee"] is None

    # Verify second
    assert data[1]["id"] == c1.id
    assert data[1]["commune"] == "Montmédy"
    assert data[1]["suivi_procedure"]["observations_internes"] == "Some notes"


@pytest.mark.django_db
def test_backoffice_staff_list(client):
    admin_user = UserFactory(is_staff=True, first_name="Jennifer", last_name="Dupont")
    staff_user = UserFactory(is_staff=True, first_name="Anthony", last_name="Martin")
    regular_user = UserFactory(is_staff=False, first_name="John", last_name="Doe")
    client.force_login(admin_user)
    url = reverse("backoffice-staff-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assignees = response.json()
    # Must contain both staff members and not regular user
    names = [a["name"] for a in assignees]
    assert "Jennifer Dupont" in names
    assert "Anthony Martin" in names
    assert "John Doe" not in names


@pytest.mark.django_db
def test_assign_suivi_procedure(client):
    staff_user = UserFactory(is_staff=True)
    regular_user = UserFactory(is_staff=False)
    client.force_login(staff_user)
    c = Constatation.objects.create(
        user=regular_user,
        commune="Paris",
        date_constat="2026-07-01",
    )
    sp = c.suivi_procedure
    update_url = reverse("suivi-procedure-detail", kwargs={"constatation_id": c.id})
    payload = {
        "personne_assignee": staff_user.id,
        "observations_internes": "Updated note",
    }
    response = client.patch(update_url, payload, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    sp.refresh_from_db()
    assert sp.personne_assignee == staff_user
    assert sp.date_pilotage is not None
    assert sp.observations_internes == "Updated note"


@pytest.mark.django_db
def test_unassign_suivi_procedure(client):
    staff_user = UserFactory(is_staff=True)
    regular_user = UserFactory(is_staff=False)
    client.force_login(staff_user)
    c = Constatation.objects.create(
        user=regular_user,
        commune="Paris",
        date_constat="2026-07-01",
    )
    sp = c.suivi_procedure
    sp.personne_assignee = staff_user
    sp.save()
    update_url = reverse("suivi-procedure-detail", kwargs={"constatation_id": c.id})
    payload = {
        "personne_assignee": None,
    }
    response = client.patch(update_url, payload, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    sp.refresh_from_db()
    assert sp.personne_assignee is None


@pytest.mark.django_db
def test_backoffice_dashboard_stats(client):
    staff_user = UserFactory(is_staff=True)
    client.force_login(staff_user)

    # 1. Excluded test
    c_test = Constatation.objects.create(
        user=staff_user,
        commune="Test Commune",
        ceci_est_un_test=True,
    )
    sp_test = c_test.suivi_procedure
    sp_test.etape_en_cours = 1
    sp_test.save()

    # 2. Active procedure (etape < 5, not archived)
    c_active = Constatation.objects.create(
        user=staff_user,
        commune="Active",
        ceci_est_un_test=False,
    )
    sp_active = c_active.suivi_procedure
    sp_active.etape_en_cours = 1
    sp_active.dossier_archive = False
    sp_active.save()

    # 3. AR waiting (etape < 5, letter_envoyee=True, ar_recu=False)
    c_ar = Constatation.objects.create(
        user=staff_user,
        commune="AR Waiting",
        ceci_est_un_test=False,
    )
    sp_ar = c_ar.suivi_procedure
    sp_ar.etape_en_cours = 2
    sp_ar.lettre_envoyee = True
    sp_ar.ar_recu = False
    sp_ar.save()

    # 4. Decision to take (etape = 3)
    c_dec = Constatation.objects.create(
        user=staff_user,
        commune="Decision",
        ceci_est_un_test=False,
    )
    sp_dec = c_dec.suivi_procedure
    sp_dec.etape_en_cours = 3
    sp_dec.save()

    # 5. Closed (statut_traitement = "Clôturé")
    c_closed = Constatation.objects.create(
        user=staff_user,
        commune="Closed",
        ceci_est_un_test=False,
    )
    sp_closed = c_closed.suivi_procedure
    sp_closed.statut_traitement = "Clôturé"
    sp_closed.etape_en_cours = 5
    sp_closed.save()

    url = reverse("backoffice-dashboard-stats-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["totalActive"] == 3
    assert data["arWaiting"] == 1
    assert data["decisionToTake"] == 1
    assert data["closed"] == 1


@pytest.mark.django_db
def test_regular_user_cannot_update_backoffice_fields(client):
    staff_user = UserFactory(is_staff=True)
    regular_user = UserFactory(is_staff=False)
    client.force_login(regular_user)

    # Create a constatation owned by regular_user
    c = Constatation.objects.create(
        user=regular_user,
        commune="Paris",
        date_constat="2026-07-01",
    )
    sp = c.suivi_procedure

    update_url = reverse("suivi-procedure-detail", kwargs={"constatation_id": c.id})

    # 1. Try to modify staff-only field `personne_assignee`
    payload = {
        "personne_assignee": staff_user.id,
    }
    response = client.patch(update_url, payload, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    sp.refresh_from_db()
    assert sp.personne_assignee is None

    # 2. Try to modify staff-only field `statut_traitement`
    payload = {
        "statut_traitement": "En cours",
    }
    response = client.patch(update_url, payload, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    sp.refresh_from_db()
    assert sp.statut_traitement == "Nouveau"

    # 3. Modify user-writable field `observations_internes` (allowed)
    payload = {
        "observations_internes": "Allowed user note",
    }
    response = client.patch(update_url, payload, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    sp.refresh_from_db()
    assert sp.observations_internes == "Allowed user note"

    # 4. Try to modify staff-only field `notes_traitement` (disallowed)
    payload = {
        "notes_traitement": "Disallowed note",
    }
    response = client.patch(update_url, payload, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    sp.refresh_from_db()
    assert sp.notes_traitement == ""


@pytest.mark.django_db
def test_backoffice_procedures_filter_besoin_accompagnement(client):
    staff_user = UserFactory(is_staff=True)
    client.force_login(staff_user)
    avec_accompagnement = Constatation.objects.create(
        user=staff_user,
        commune="Montmédy",
        date_constat="2026-06-27",
        constatant_role="Secrétaire de mairie",
        ceci_est_un_test=False,
        besoin_accompagnement=True,
    )
    sans_accompagnement = Constatation.objects.create(
        user=staff_user,
        commune="Fécamp",
        date_constat="2026-05-27",
        constatant_role="Gendarme",
        ceci_est_un_test=False,
        besoin_accompagnement=False,
    )
    url = reverse("backoffice-procedures-list")
    def ids_for(params):
        response = client.get(url, params)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        results = data["results"] if isinstance(data, dict) and "results" in data else data
        return {item["id"] for item in results}
    assert ids_for({}) == {avec_accompagnement.id, sans_accompagnement.id}
    assert ids_for({"besoin_accompagnement": "Oui"}) == {avec_accompagnement.id}
    assert ids_for({"besoinAccompagnement": "Oui"}) == {avec_accompagnement.id}
    assert ids_for({"besoinAccompagnement": "Non"}) == {sans_accompagnement.id}


@pytest.mark.django_db
def test_backoffice_users_permissions(client):
    url = reverse("backoffice-users-list")
    # Anonymous
    response = client.get(url)
    assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    # Non staff
    user = UserFactory(is_staff=False)
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_backoffice_users_list_and_filters(client):
    from backend.proconnect.models import ProConnectProfile

    staff_user = UserFactory(is_staff=True, email="staff@beta.gouv.fr")
    client.force_login(staff_user)

    user_without_proc = UserFactory(
        email="zero_proc@test.com", first_name="Alice", last_name="Dupont"
    )
    user_with_proc = UserFactory(
        email="with_proc@test.com", first_name="Bob", last_name="Martin"
    )
    Constatation.objects.create(
        user=user_with_proc,
        commune="Paris",
        date_constat="2026-06-27",
        constatant_role="Garde champêtre",
        ceci_est_un_test=False,
    )

    ProConnectProfile.objects.create(
        user=user_with_proc,
        siret="12345678900012",
        siren="123456789",
        organization_label="Mairie de Paris",
        roles=["agent_public"],
    )

    url = reverse("backoffice-users-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    results = data["results"] if isinstance(data, dict) and "results" in data else data
    emails = [u["email"] for u in results]
    assert "zero_proc@test.com" in emails
    assert "with_proc@test.com" in emails

    bob_data = next(u for u in results if u["email"] == "with_proc@test.com")
    assert bob_data["procedures_count"] == 1
    assert bob_data["has_proconnect"] is True
    assert bob_data["proconnect_profile"]["siret"] == "12345678900012"
    assert bob_data["proconnect_profile"]["organization_label"] == "Mairie de Paris"

    alice_data = next(u for u in results if u["email"] == "zero_proc@test.com")
    assert alice_data["procedures_count"] == 0
    assert alice_data["has_proconnect"] is False
    assert alice_data["proconnect_profile"] is None

    # Filter by has_procedures=Non
    res_no_proc = client.get(url, {"has_procedures": "Non"}).json()
    res_no_proc_emails = [u["email"] for u in res_no_proc.get("results", res_no_proc)]
    assert "zero_proc@test.com" in res_no_proc_emails
    assert "with_proc@test.com" not in res_no_proc_emails

    # Filter by has_procedures=Oui
    res_has_proc = client.get(url, {"has_procedures": "Oui"}).json()
    res_has_proc_emails = [u["email"] for u in res_has_proc.get("results", res_has_proc)]
    assert "with_proc@test.com" in res_has_proc_emails
    assert "zero_proc@test.com" not in res_has_proc_emails

    # Filter by has_proconnect=Oui
    res_pc = client.get(url, {"has_proconnect": "Oui"}).json()
    res_pc_emails = [u["email"] for u in res_pc.get("results", res_pc)]
    assert "with_proc@test.com" in res_pc_emails
    assert "zero_proc@test.com" not in res_pc_emails

    # Filter search by siret
    res_search = client.get(url, {"search": "12345678900012"}).json()
    res_search_emails = [u["email"] for u in res_search.get("results", res_search)]
    assert "with_proc@test.com" in res_search_emails
    assert "zero_proc@test.com" not in res_search_emails


@pytest.mark.django_db
def test_backoffice_users_export_csv(client):
    from backend.proconnect.models import ProConnectProfile

    staff_user = UserFactory(is_staff=True, email="staff2@beta.gouv.fr")
    client.force_login(staff_user)

    user = UserFactory(email="test_csv@test.com", first_name="Claire", last_name="Fontaine")
    ProConnectProfile.objects.create(
        user=user,
        siret="98765432100011",
        siren="987654321",
        organization_label="Communauté de communes",
        roles=["agent_public"],
    )

    url = reverse("backoffice-users-export-csv")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response["Content-Type"].startswith("text/csv")
    content = response.content.decode("utf-8-sig")
    assert "Identifiant;E-mail;Prénom;Nom" in content
    assert "test_csv@test.com" in content
    assert "98765432100011" in content
    assert "Communauté de communes" in content

    # Test with filter on CSV export
    response_filtered = client.get(url, {"has_procedures": "Oui"})
    content_filtered = response_filtered.content.decode("utf-8-sig")
    assert "test_csv@test.com" not in content_filtered
