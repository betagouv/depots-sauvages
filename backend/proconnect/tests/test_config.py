import pytest
from django.core.management import call_command

from backend.proconnect.models import ProConnectAccessConfig


@pytest.fixture(autouse=True)
def load_proconnect_fixture(db):
    call_command("loaddata", "proconnect_access_config")


@pytest.mark.django_db
def test_proconnect_access_config_fixture():
    config = ProConnectAccessConfig.get_solo()
    assert config is not None
    assert len(config.categories_juridiques_autorisees) == 5
    codes = [item["code"] for item in config.categories_juridiques_autorisees]
    assert "72" in codes
    assert "734" in codes
    assert "735" in codes
    assert "7361" in codes

    sirens = [item["siren"] for item in config.sirens_autorises]
    assert "157000019" in sirens  # Gendarmerie
    assert "662043116" in sirens  # ONF
    assert "130025943" in sirens  # OFB
    assert "130025265" in sirens  # DINUM


@pytest.mark.django_db
def test_is_siren_allowed():
    config = ProConnectAccessConfig.get_solo()
    # SIREN authorized by default (e.g. Gendarmerie)
    assert config.is_siren_allowed("157000019") is True
    # Unknown SIREN
    assert config.is_siren_allowed("999999999") is False
    # Adding a SIREN with label dictionary
    config.sirens_autorises.append({"siren": "999999999", "nom": "Organisme Test"})
    config.save()
    assert config.is_siren_allowed("999999999") is True
    # Also supports adding raw string (admin fallback flexibility)
    config.sirens_autorises.append("888888888")
    config.save()
    assert config.is_siren_allowed("888888888") is True


@pytest.mark.django_db
def test_is_legal_category_allowed():
    config = ProConnectAccessConfig.get_solo()
    assert config.is_legal_category_allowed("7210") is True  # Municipality
    assert config.is_legal_category_allowed("7346") is True  # Community of municipalities
    assert config.is_legal_category_allowed("7354") is True  # Mixed syndicate
    assert config.is_legal_category_allowed("7361") is True  # CCAS
    assert config.is_legal_category_allowed("7331") is False  # School / Rectorate
    assert (
        config.is_legal_category_allowed("7150") is False
    )  # Deconcentrated service without whitelist
    assert config.is_legal_category_allowed("") is False
    assert config.is_legal_category_allowed(None) is False
    config.categories_juridiques_autorisees = [{"code": "", "nom": ""}, ""]
    config.save()
    assert config.is_legal_category_allowed("7150") is False
    assert config.is_legal_category_allowed("5499") is False
