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

    url = reverse("backoffice-procedures-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2

    # Verify first (c2 is newer / higher ID, so first in order-by "-id")
    assert data[0]["id"] == c2.id
    assert data[0]["commune"] == "Fécamp"
    assert data[0]["user_email"] == staff_user.email
    assert data[0]["suivi_procedure"]["etape_en_cours"] == 1
    assert data[0]["suivi_procedure"]["assigned_to"] is None

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
        "assigned_to": staff_user.id,
        "observations_internes": "Updated note",
    }
    response = client.patch(update_url, payload, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    sp.refresh_from_db()
    assert sp.assigned_to == staff_user
    assert sp.assigned_at is not None
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
    sp.assigned_to = staff_user
    sp.save()
    update_url = reverse("suivi-procedure-detail", kwargs={"constatation_id": c.id})
    payload = {
        "assigned_to": None,
    }
    response = client.patch(update_url, payload, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    sp.refresh_from_db()
    assert sp.assigned_to is None
