import pytest
from django.urls import reverse
from rest_framework import status

from backend.constatations.models import Constatation
from backend.procedures.models import SuiviProcedure
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
    assert data[0]["suivi_procedure"]["charge_deploiement"] == "Non assigné"

    # Verify second
    assert data[1]["id"] == c1.id
    assert data[1]["commune"] == "Montmédy"
    assert data[1]["suivi_procedure"]["observations_internes"] == "Some notes"
