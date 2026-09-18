import datetime
from decimal import Decimal

import pytest

from backend.stats.collectors import tally

FORM_UTILISABILITE = {
    "form_id": "VLArqN",
    "metric": "utilisabilite_constatation",
    "question_id": "",
    "question_contains": "",
    "scale": "note_1_5",
}
FORM_UTILITE = {
    "form_id": "OD9RMg",
    "metric": "utilite_procedure",
    "question_id": "",
    "question_contains": "plus facilement",
    "scale": "accord_5",
}

ACCORD_OPTIONS = [
    {"id": "opt1", "text": "Tout à fait d'accord"},
    {"id": "opt2", "text": "Plutôt d'accord"},
    {"id": "opt3", "text": "Ni d'accord ni pas d'accord"},
    {"id": "opt4", "text": "Plutôt pas d'accord"},
    {"id": "opt5", "text": "Pas du tout d'accord"},
]


def submission(submitted_at, question_id, value):
    return {
        "id": f"sub-{submitted_at}-{value}",
        "isCompleted": True,
        "submittedAt": submitted_at,
        "responses": [{"questionId": question_id, "value": value}],
    }


class FakeSession:
    """Remplace requests.Session : rend les pages préparées, dans l'ordre."""

    def __init__(self, pages):
        self.pages = list(pages)
        self.headers = {}
        self.calls = []

    def get(self, url, params=None, timeout=None):
        self.calls.append((url, params))
        payload = self.pages[min(params["page"], len(self.pages)) - 1]
        return FakeResponse(payload)


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


@pytest.fixture
def patch_session(monkeypatch):
    def _patch(pages):
        session = FakeSession(pages)
        monkeypatch.setattr(tally.requests, "Session", lambda: session)
        monkeypatch.setattr(tally.time, "sleep", lambda _seconds: None)
        return session

    return _patch


@pytest.fixture(autouse=True)
def tally_settings(settings):
    settings.TALLY_API_KEY = "test-key"
    settings.TALLY_FORMS = [FORM_UTILISABILITE]
    return settings


def test_collect_compte_les_notes_par_jour_et_par_valeur(patch_session):
    patch_session(
        [
            {
                "hasMore": False,
                "questions": [{"id": "q1", "type": "RATING", "title": "Cet outil était-il simple"}],
                "submissions": [
                    submission("2026-09-15T10:00:00.000Z", "q1", 5),
                    submission("2026-09-15T11:00:00.000Z", "q1", 5),
                    submission("2026-09-15T12:00:00.000Z", "q1", 4),
                    submission("2026-09-16T09:00:00.000Z", "q1", 3),
                ],
            }
        ]
    )

    points = tally.collect(datetime.date(2026, 9, 14), datetime.date(2026, 9, 16))

    resultats = {(point.date, point.dimension): point.value for point in points}
    assert resultats == {
        (datetime.date(2026, 9, 15), "4"): Decimal(1),
        (datetime.date(2026, 9, 15), "5"): Decimal(2),
        (datetime.date(2026, 9, 16), "3"): Decimal(1),
    }
    assert {point.metric for point in points} == {"utilisabilite_constatation"}
    assert {point.source for point in points} == {"tally"}


def test_collect_ignore_les_reponses_hors_fenetre(patch_session):
    patch_session(
        [
            {
                "hasMore": False,
                "questions": [{"id": "q1", "type": "RATING", "title": "Note"}],
                "submissions": [
                    submission("2026-09-10T10:00:00.000Z", "q1", 5),
                    submission("2026-09-15T10:00:00.000Z", "q1", 4),
                    submission("2026-09-20T10:00:00.000Z", "q1", 3),
                ],
            }
        ]
    )

    points = tally.collect(datetime.date(2026, 9, 14), datetime.date(2026, 9, 16))

    assert [(point.date, point.dimension) for point in points] == [
        (datetime.date(2026, 9, 15), "4")
    ]


def test_collect_ignore_une_note_hors_echelle(patch_session, caplog):
    patch_session(
        [
            {
                "hasMore": False,
                "questions": [{"id": "q1", "type": "RATING", "title": "Note"}],
                "submissions": [
                    submission("2026-09-15T10:00:00.000Z", "q1", 4),
                    submission("2026-09-15T11:00:00.000Z", "q1", 9),
                    submission("2026-09-15T12:00:00.000Z", "q1", None),
                ],
            }
        ]
    )

    points = tally.collect(datetime.date(2026, 9, 15), datetime.date(2026, 9, 15))

    assert [(point.dimension, point.value) for point in points] == [("4", Decimal(1))]
    assert "non reconnue" in caplog.text


def test_collect_traduit_les_modalites_daccord(patch_session, settings):
    settings.TALLY_FORMS = [FORM_UTILITE]
    patch_session(
        [
            {
                "hasMore": False,
                "questions": [
                    {
                        "id": "q7",
                        "type": "MULTIPLE_CHOICE",
                        "title": (
                            "Stop Dépôt Sauvage m'a permis d'engager cette "
                            "procédure plus facilement."
                        ),
                        "options": ACCORD_OPTIONS,
                    }
                ],
                "submissions": [
                    submission("2026-09-15T10:00:00.000Z", "q7", ["opt1"]),
                    submission("2026-09-15T11:00:00.000Z", "q7", ["opt2"]),
                    submission("2026-09-15T12:00:00.000Z", "q7", ["opt4"]),
                    submission("2026-09-15T13:00:00.000Z", "q7", ["opt1"]),
                ],
            }
        ]
    )

    points = tally.collect(datetime.date(2026, 9, 15), datetime.date(2026, 9, 15))

    assert {point.dimension: point.value for point in points} == {
        "tout_a_fait_daccord": Decimal(2),
        "plutot_daccord": Decimal(1),
        "plutot_pas_daccord": Decimal(1),
    }


def test_collect_alerte_si_une_modalite_est_inconnue(patch_session, settings, caplog):
    settings.TALLY_FORMS = [FORM_UTILITE]
    patch_session(
        [
            {
                "hasMore": False,
                "questions": [
                    {
                        "id": "q7",
                        "type": "MULTIPLE_CHOICE",
                        "title": "Cette procédure plus facilement ?",
                        "options": [
                            {"id": "opt1", "text": "Tout à fait d'accord"},
                            {"id": "opt9", "text": "Sans opinion"},
                        ],
                    }
                ],
                "submissions": [
                    submission("2026-09-15T10:00:00.000Z", "q7", ["opt1"]),
                    submission("2026-09-15T11:00:00.000Z", "q7", ["opt9"]),
                ],
            }
        ]
    )

    points = tally.collect(datetime.date(2026, 9, 15), datetime.date(2026, 9, 15))

    assert {point.dimension: point.value for point in points} == {"tout_a_fait_daccord": Decimal(1)}
    assert "Sans opinion" in caplog.text


def test_collect_alerte_si_la_question_a_disparu(patch_session, settings, caplog):
    settings.TALLY_FORMS = [FORM_UTILITE]
    patch_session(
        [
            {
                "hasMore": False,
                "questions": [
                    {"id": "q1", "type": "INPUT_TEXT", "title": "Votre commune"},
                    {"id": "q2", "type": "INPUT_TEXT", "title": "Vos remarques"},
                ],
                "submissions": [submission("2026-09-15T10:00:00.000Z", "q1", "Lyon")],
            }
        ]
    )

    points = tally.collect(datetime.date(2026, 9, 15), datetime.date(2026, 9, 15))

    assert points == []
    assert "question introuvable" in caplog.text


def test_collect_sarrete_quand_la_page_est_anterieure_a_la_fenetre(patch_session):
    session = patch_session(
        [
            {
                "hasMore": True,
                "questions": [{"id": "q1", "type": "RATING", "title": "Note"}],
                "submissions": [submission("2026-09-15T10:00:00.000Z", "q1", 5)],
            },
            {
                "hasMore": True,
                "questions": [{"id": "q1", "type": "RATING", "title": "Note"}],
                "submissions": [submission("2026-08-01T10:00:00.000Z", "q1", 5)],
            },
            {
                "hasMore": True,
                "questions": [{"id": "q1", "type": "RATING", "title": "Note"}],
                "submissions": [submission("2026-07-01T10:00:00.000Z", "q1", 5)],
            },
        ]
    )

    tally.collect(datetime.date(2026, 9, 14), datetime.date(2026, 9, 16))

    # La page 3 n'est jamais demandée : la page 2 est déjà entièrement hors fenêtre.
    assert [params["page"] for _url, params in session.calls] == [1, 2]


def test_collect_sans_cle_api_leve_une_erreur_explicite(settings):
    settings.TALLY_API_KEY = ""

    with pytest.raises(tally.TallyConfigurationError, match="TALLY_API_KEY"):
        tally.collect(datetime.date(2026, 9, 15), datetime.date(2026, 9, 15))
