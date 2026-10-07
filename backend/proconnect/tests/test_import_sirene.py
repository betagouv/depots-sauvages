import io
import zipfile
from unittest.mock import MagicMock, patch

import pytest
from django.core.management import call_command

from backend.proconnect.management.commands.import_sirene_public import parse_csv_stream
from backend.proconnect.models import PublicEntitySirene


@pytest.mark.django_db
def test_parse_csv_stream_filters_and_saves_public_entities():
    csv_content = (
        "siren,categorieJuridiqueUniteLegale,denominationUniteLegale,denominationUsuelle1UniteLegale\n"
        "217500016,7210,COMMUNE DE PARIS,\n"
        "123456789,5710,ENTREPRISE PRIVEE SAS,\n"
        "200054781,7344,METROPOLE DU GRAND PARIS,\n"
        "999999999,7361,,CCAS DE TEST\n"
        ",7210,SANS SIREN,\n"
    )
    stream = io.StringIO(csv_content)
    count = parse_csv_stream(stream, batch_size=2)
    assert count == 3
    paris = PublicEntitySirene.objects.filter(siren="217500016").first()
    assert paris is not None
    assert paris.categorie_juridique == "7210"
    assert paris.denomination == "COMMUNE DE PARIS"
    metropole = PublicEntitySirene.objects.filter(siren="200054781").first()
    assert metropole is not None
    assert metropole.categorie_juridique == "7344"
    assert metropole.denomination == "METROPOLE DU GRAND PARIS"
    ccas = PublicEntitySirene.objects.filter(siren="999999999").first()
    assert ccas is not None
    assert ccas.categorie_juridique == "7361"
    assert ccas.denomination == "CCAS DE TEST"
    assert not PublicEntitySirene.objects.filter(siren="123456789").exists()


@pytest.mark.django_db
def test_import_sirene_public_command_file(tmp_path):
    csv_content = (
        "siren,categorieJuridiqueUniteLegale,denominationUniteLegale,denominationUsuelle1UniteLegale\n"
        "216901231,7210,VILLE DE LYON,\n"
    )
    file_path = tmp_path / "test_sirene.csv"
    file_path.write_text(csv_content, encoding="utf-8")
    call_command("import_sirene_public", f"--file={file_path}")
    lyon = PublicEntitySirene.objects.filter(siren="216901231").first()
    assert lyon is not None
    assert lyon.denomination == "VILLE DE LYON"


@pytest.mark.django_db
def test_import_sirene_public_command_zip_file(tmp_path):
    csv_content = (
        "siren,categorieJuridiqueUniteLegale,denominationUniteLegale,denominationUsuelle1UniteLegale\n"
        "211300553,7210,VILLE DE MARSEILLE,\n"
    )
    zip_path = tmp_path / "test_sirene.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("StockUniteLegale_utf8.csv", csv_content)
    call_command("import_sirene_public", f"--file={zip_path}")
    marseille = PublicEntitySirene.objects.filter(siren="211300553").first()
    assert marseille is not None
    assert marseille.denomination == "VILLE DE MARSEILLE"
