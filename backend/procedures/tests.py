import pytest
from django.urls import reverse
from rest_framework import status

from backend.constatations.models import Constatation
from backend.procedures.models import SuiviProcedure
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
    }
    response = client.put(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    suivi.refresh_from_db()
    assert suivi.etape_en_cours == 2
    assert suivi.preuves_fournies is True


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
