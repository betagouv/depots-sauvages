import datetime
from decimal import Decimal
from io import StringIO

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from backend.stats.collectors import MetricPoint
from backend.stats.management.commands import sync_external_metrics
from backend.stats.models import ExternalMetric

JOUR = datetime.date(2026, 9, 15)


def point(dimension, value, metric="utilisabilite_constatation"):
    return MetricPoint(
        source="tally",
        metric=metric,
        date=JOUR,
        dimension=dimension,
        value=Decimal(value),
        details={"form_id": "VLArqN"},
    )


@pytest.fixture
def collectors(monkeypatch):
    """Remplace le registre des collecteurs par des doublures pilotables."""

    def _install(registry):
        monkeypatch.setattr(sync_external_metrics, "COLLECTORS", registry)
        return registry

    return _install


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_ecrit_les_points_collectes(collectors):
    collectors({"tally": lambda start, end: [point("4", 1), point("5", 3)]})
    out = StringIO()

    call_command("sync_external_metrics", stdout=out)

    assert "finished successfully" in out.getvalue()
    lignes = ExternalMetric.objects.using("stats_db").order_by("dimension")
    assert [(ligne.dimension, ligne.value) for ligne in lignes] == [
        ("4", Decimal("1.00")),
        ("5", Decimal("3.00")),
    ]


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_relancer_la_commande_ne_cree_pas_de_doublon(collectors):
    collectors({"tally": lambda start, end: [point("5", 3)]})
    call_command("sync_external_metrics", stdout=StringIO())

    collectors({"tally": lambda start, end: [point("5", 7)]})
    call_command("sync_external_metrics", stdout=StringIO())

    assert ExternalMetric.objects.using("stats_db").count() == 1
    assert ExternalMetric.objects.using("stats_db").get().value == Decimal("7.00")


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_dry_run_nectit_rien(collectors):
    collectors({"tally": lambda start, end: [point("5", 3)]})
    out = StringIO()

    call_command("sync_external_metrics", "--dry-run", stdout=out)

    assert "[dry-run]" in out.getvalue()
    assert ExternalMetric.objects.using("stats_db").count() == 0


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_la_fenetre_depend_de_loption_days(collectors):
    fenetres = []

    def collecteur(start, end):
        fenetres.append((start, end))
        return []

    collectors({"tally": collecteur})

    call_command("sync_external_metrics", "--days", "30", stdout=StringIO())

    start, end = fenetres[0]
    assert (end - start).days == 29


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_une_source_en_echec_nempeche_pas_les_autres(collectors):
    def casse(start, end):
        raise RuntimeError("API indisponible")

    collectors({"tally": lambda start, end: [point("5", 3)], "matomo": casse})
    out, err = StringIO(), StringIO()

    call_command("sync_external_metrics", stdout=out, stderr=err)

    assert "API indisponible" in err.getvalue()
    assert "Collecte terminée avec des échecs" in out.getvalue()
    assert ExternalMetric.objects.using("stats_db").count() == 1


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_echec_de_toutes_les_sources_fait_echouer_la_commande(collectors):
    def casse(start, end):
        raise RuntimeError("API indisponible")

    collectors({"tally": casse})

    with pytest.raises(CommandError, match="Aucune source"):
        call_command("sync_external_metrics", stdout=StringIO(), stderr=StringIO())


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_ne_collecte_rien_si_les_stats_sont_desactivees(collectors, settings):
    settings.STATS_ENABLED = False
    collectors({"tally": lambda start, end: [point("5", 3)]})
    out = StringIO()

    call_command("sync_external_metrics", stdout=out)

    assert "Stats feature is disabled" in out.getvalue()
    assert ExternalMetric.objects.using("stats_db").count() == 0
