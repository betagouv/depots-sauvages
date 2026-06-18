import io
import pytest
from django.core.management import call_command

from backend.constatations.models import Constatation


@pytest.mark.django_db
def test_regenerate_constatation_docs_dry_run():
    # Create two constatations: one with auteur_identifie = True, one False
    c1 = Constatation.objects.create(
        commune="Paris",
        auteur_identifie=True,
        doc_constat_should_generate=False,
        lettre_info_should_generate=False,
    )
    c2 = Constatation.objects.create(
        commune="Lyon",
        auteur_identifie=False,
        doc_constat_should_generate=False,
        lettre_info_should_generate=False,
    )

    out = io.StringIO()
    call_command("regenerate_constatation_docs", "--dry-run", stdout=out)

    # Dry-run should not save flags to DB
    c1.refresh_from_db()
    c2.refresh_from_db()
    assert not c1.doc_constat_should_generate
    assert not c1.lettre_info_should_generate
    assert not c2.doc_constat_should_generate
    assert not c2.lettre_info_should_generate

    output = out.getvalue()
    assert "SIMULATION (DRY-RUN) TERMINEE AVEC SUCCES" in output


@pytest.mark.django_db
def test_regenerate_constatation_docs_all(mocker):
    # Mock the tasks/signals to prevent background execution in tests
    mock_generate = mocker.patch("backend.constatations.signals.generate_document")

    c1 = Constatation.objects.create(
        commune="Paris",
        auteur_identifie=True,
        doc_constat_should_generate=False,
        lettre_info_should_generate=False,
    )
    c2 = Constatation.objects.create(
        commune="Lyon",
        auteur_identifie=False,
        doc_constat_should_generate=False,
        lettre_info_should_generate=False,
    )

    out = io.StringIO()
    call_command("regenerate_constatation_docs", stdout=out)

    c1.refresh_from_db()
    c2.refresh_from_db()

    # c1 has auteur_identifie = True, so both should generate
    assert c1.doc_constat_should_generate
    assert c1.lettre_info_should_generate

    # c2 has auteur_identifie = False, so only doc_constat should generate
    assert c2.doc_constat_should_generate
    assert not c2.lettre_info_should_generate

    # Verify generate was called
    # c1: once for doc_constat, once for lettre_info.
    # c2: once for doc_constat.
    assert mock_generate.call_count == 3


@pytest.mark.django_db
def test_regenerate_constatation_docs_only_constat(mocker):
    mock_generate = mocker.patch("backend.constatations.signals.generate_document")

    c1 = Constatation.objects.create(
        commune="Paris",
        auteur_identifie=True,
        doc_constat_should_generate=False,
        lettre_info_should_generate=False,
    )

    out = io.StringIO()
    call_command("regenerate_constatation_docs", "--only-constat", stdout=out)

    c1.refresh_from_db()
    assert c1.doc_constat_should_generate
    assert not c1.lettre_info_should_generate
    assert mock_generate.call_count == 1


@pytest.mark.django_db
def test_regenerate_constatation_docs_only_lettre(mocker):
    mock_generate = mocker.patch("backend.constatations.signals.generate_document")

    c1 = Constatation.objects.create(
        commune="Paris",
        auteur_identifie=True,
        doc_constat_should_generate=False,
        lettre_info_should_generate=False,
    )
    c2 = Constatation.objects.create(
        commune="Lyon",
        auteur_identifie=False,
        doc_constat_should_generate=False,
        lettre_info_should_generate=False,
    )

    out = io.StringIO()
    call_command("regenerate_constatation_docs", "--only-lettre", stdout=out)

    c1.refresh_from_db()
    c2.refresh_from_db()

    assert not c1.doc_constat_should_generate
    assert c1.lettre_info_should_generate

    assert not c2.doc_constat_should_generate
    assert not c2.lettre_info_should_generate

    assert mock_generate.call_count == 1
