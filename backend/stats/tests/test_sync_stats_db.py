from io import StringIO

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from backend.constatations.models import Constatation
from backend.stats.models import StatsConstatation, StatsSuiviProcedure

User = get_user_model()


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_sync_stats_db_command_full_and_incremental():
    u1 = User.objects.create_user(username="agent1", email="agent1@example.com")
    c1 = Constatation.objects.using("default").create(
        user=u1,
        commune="Lyon",
        constatant_nom="Dupont",
        constatant_prenom="Jean",
        contact_email="jean.dupont@example.com",
        contact_telephone="0601020304",
        doc_constat=b"PDF_BINARY_DATA",
        lettre_info=b"LETTRE_BINARY_DATA",
    )
    s1 = c1.suivi_procedure
    s1.observations_internes = "Remarque confidentielle"
    s1.save()
    out = StringIO()
    call_command("sync_stats_db", "--full-reset", stdout=out)
    assert "Stats database synchronization finished successfully." in out.getvalue()
    stats_c1 = StatsConstatation.objects.using("stats_db").get(id=c1.id)
    assert stats_c1.commune == "Lyon"
    assert stats_c1.user_hash != ""
    assert stats_c1.user_hash is not None
    assert str(u1.id) not in stats_c1.user_hash
    assert stats_c1.contact_email.startswith("anon_")
    assert "jean.dupont" not in stats_c1.contact_email
    assert stats_c1.contact_telephone == ""
    assert not hasattr(stats_c1, "doc_constat")
    assert not hasattr(stats_c1, "lettre_info")
    stats_s1 = StatsSuiviProcedure.objects.using("stats_db").get(id=s1.id)
    assert stats_s1.constatation_id == c1.id
    assert stats_s1.observations_internes == "[ANONYMIZED]"

    c2 = Constatation.objects.using("default").create(
        commune="Marseille",
        constatant_nom="Martin",
        contact_email="martin@example.com",
    )
    out_inc = StringIO()
    call_command("sync_stats_db", stdout=out_inc)
    assert StatsConstatation.objects.using("stats_db").count() == 2
    stats_c2 = StatsConstatation.objects.using("stats_db").get(id=c2.id)
    assert stats_c2.commune == "Marseille"
    assert stats_c2.user_hash == ""


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_sync_stats_db_disabled(settings):
    settings.STATS_ENABLED = False
    out = StringIO()
    call_command("sync_stats_db", stdout=out)
    assert (
        "Stats feature is disabled (STATS_ENABLED=False). Skipping synchronization."
        in out.getvalue()
    )
