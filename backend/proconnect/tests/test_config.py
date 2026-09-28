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
def test_est_siren_autorise():
    config = ProConnectAccessConfig.get_solo()
    # SIREN autorisé par défaut (ex: Gendarmerie)
    assert config.est_siren_autorise("157000019") is True
    # SIREN inconnu
    assert config.est_siren_autorise("999999999") is False
    # Ajout d'un SIREN avec libellé
    config.sirens_autorises.append({"siren": "999999999", "nom": "Organisme Test"})
    config.save()
    assert config.est_siren_autorise("999999999") is True
    # Supporte aussi l'ajout sous forme de string brute (flexibilité admin)
    config.sirens_autorises.append("888888888")
    config.save()
    assert config.est_siren_autorise("888888888") is True


@pytest.mark.django_db
def test_est_categorie_juridique_autorisee():
    config = ProConnectAccessConfig.get_solo()
    assert config.est_categorie_juridique_autorisee("7210") is True  # Commune
    assert config.est_categorie_juridique_autorisee("7346") is True  # CC
    assert config.est_categorie_juridique_autorisee("7354") is True  # Syndicat mixte
    assert config.est_categorie_juridique_autorisee("7361") is True  # CCAS
    assert config.est_categorie_juridique_autorisee("7331") is False  # Collège / Rectorat
    assert (
        config.est_categorie_juridique_autorisee("7150") is False
    )  # Service déconcentré hors whitelist
