import pytest
from django.core.management import CommandError, call_command
from django.test import override_settings

from backend.constatations.models import Constatation


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_create_demo_procedures_creates_and_resets():
    call_command("create_demo_procedures", email="demo@example.com")
    qs = Constatation.objects.filter(user__username="demo@example.com")
    nb = qs.count()
    assert nb >= 15
    assert all(c.ceci_est_un_test for c in qs)
    assert qs.filter(auteur_nom="Dupont").get().suivi_procedure.ar_presentation_date is not None
    # --reset ne duplique pas les dossiers
    call_command("create_demo_procedures", email="demo@example.com", reset=True)
    assert qs.count() == nb


@pytest.mark.django_db(databases=["default", "stats_db"])
@override_settings(ENV_NAME="prod")
def test_create_demo_procedures_forbidden_in_production():
    with pytest.raises(CommandError):
        call_command("create_demo_procedures", email="demo@example.com")
    assert not Constatation.objects.exists()


@pytest.mark.django_db(databases=["default", "stats_db"])
@override_settings(ENV_NAME="unknown_env")
def test_create_demo_procedures_forbidden_in_unknown_env():
    with pytest.raises(CommandError):
        call_command("create_demo_procedures", email="demo@example.com")
    assert not Constatation.objects.exists()

