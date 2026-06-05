import datetime
from unittest.mock import MagicMock

import pytest
from django.utils import timezone

from backend.doc_maker.odt_utils import prepare_context


@pytest.fixture
def mock_instance():
    instance = MagicMock()
    # Mocking model_to_dict behavior by letting MagicMock behave like a model instance
    # in model_to_dict. Since model_to_dict uses fields, we can mock model_to_dict using patching.
    return instance


def test_prepare_context_with_basic_fields(monkeypatch):
    # Mock model_to_dict to return a controlled dict
    initial_dict = {
        "id": 123,
        "doc_constat_should_generate": True,
        "doc_constat": b"data",
        "doc_constat_generated_at": timezone.now(),
        "lettre_info_should_generate": True,
        "lettre_info": b"letter",
        "lettre_info_generated_at": timezone.now(),
        "date_constat": datetime.date(2026, 5, 28),
        "heure_constat": datetime.time(14, 30),
        "constatant_role": "Agent de police municipale",
        "constatant_prenom": "Jean-Pierre",
        "constatant_nom": "Dupond",
        "auteur_adresse": "123 Rue de la République\n75001 Paris",
        "auteur_civilite": "M.",
        "auteur_prenom": "Marcel",
        "auteur_nom": "Martin",
    }

    monkeypatch.setattr(
        "backend.doc_maker.odt_utils.model_to_dict", lambda inst: initial_dict.copy()
    )

    mock_inst = MagicMock()
    mock_inst.get_prejudice_montant_calcule.return_value = 1500
    mock_inst.souhaite_porter_plainte = True

    context = prepare_context(mock_inst)

    # 1. Unneeded fields removed
    for field in [
        "id",
        "doc_constat_should_generate",
        "doc_constat",
        "doc_constat_generated_at",
        "lettre_info_should_generate",
        "lettre_info",
        "lettre_info_generated_at",
    ]:
        assert field not in context

    # 2. Calculated fields and basic info
    assert context["prejudice_montant_calcule"] == "1500,00"
    assert context["souhaite_porter_plainte"] is True

    # 3. Current date formatting
    today = timezone.now()
    assert context["date_courante"] == today.strftime("%-d %B %Y")
    assert context["annee_courante"] == today.year

    # 4. Constat dates and times
    assert (
        context["date_constat"] == "28 May 2026" or "28 mai 2026" in context["date_constat"].lower()
    )  # depending on locale
    assert context["heure_constat"] == "14:30"

    # 5. Elision checking (Agent starts with A, vowel)
    assert context["constatant_role_needs_elision"] is True

    # 6. Constatant name formatting
    assert context["constatant_nom_complet"] == "Jean-Pierre Dupond"

    # 7. Auteur adresse split (newline)
    assert context["auteur_adresse_l1"] == "123 Rue de la République"
    assert context["auteur_adresse_l2"] == "75001 Paris"

    # 8. Auteur name formatting
    assert context["auteur_nom_complet"] == "M. Marcel Martin"


def test_prepare_context_auteur_adresse_regex(monkeypatch):
    # Test address matching without newline
    initial_dict = {
        "auteur_adresse": "123 Rue de la République 75001 Paris",
        "constatant_role": "officier",  # starts with vowel
        "constatant_prenom": "",
        "constatant_nom": "",
        "auteur_civilite": "",
        "auteur_prenom": "Marcel",
        "auteur_nom": "Martin",
    }

    monkeypatch.setattr(
        "backend.doc_maker.odt_utils.model_to_dict", lambda inst: initial_dict.copy()
    )

    mock_inst = MagicMock()
    mock_inst.get_prejudice_montant_calcule.return_value = 0
    mock_inst.souhaite_porter_plainte = False

    context = prepare_context(mock_inst)

    assert context["auteur_adresse_l1"] == "123 Rue de la République"
    assert context["auteur_adresse_l2"] == "75001 Paris"
    assert context["constatant_role_needs_elision"] is True
    assert context["auteur_nom_complet"] == "Marcel Martin"
