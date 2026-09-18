"""Collecteur Tally — agrégats journaliers des enquêtes de satisfaction.

Deux formulaires sont collectés (voir `settings.TALLY_FORMS`) :

- l'utilisabilité du formulaire de constatation (note de 1 à 5) → KR 1.4
- l'utilité perçue de la procédure (échelle d'accord à 5 modalités) → KR 3.1.1

Ce qui entre en base : le nombre de réponses par jour et par modalité. Rien d'autre.
Les formulaires reçoivent pourtant des paramètres identifiants (commune, identifiant
de dossier) et peuvent contenir des champs libres : tout cela est ignoré ici.
"""

import datetime
import logging
import time
from collections import Counter
from decimal import Decimal

import requests
from django.conf import settings
from django.utils import timezone

from backend.stats.collectors.base import MetricPoint, normalize_label

logger = logging.getLogger(__name__)

SOURCE = "tally"
API_URL = "https://api.tally.so"
PAGE_SIZE = 100
MAX_PAGES = 200  # garde-fou : 20 000 réponses par formulaire
REQUEST_TIMEOUT = 20
PAUSE_BETWEEN_REQUESTS = 0.1  # l'API Tally est limitée à 100 requêtes/minute

NOTE_1_5 = "note_1_5"
ACCORD_5 = "accord_5"

# Les 5 modalités de l'échelle d'accord, normalisées (sans accents ni ponctuation).
ACCORD_5_MAPPING = {
    "toutafaitdaccord": "tout_a_fait_daccord",
    "plutotdaccord": "plutot_daccord",
    "nidaccordnipasdaccord": "ni_daccord_ni_pas_daccord",
    "plutotpasdaccord": "plutot_pas_daccord",
    "pasdutoutdaccord": "pas_du_tout_daccord",
}


class TallyConfigurationError(RuntimeError):
    pass


def collect(start_date, end_date):
    """Rend les effectifs de réponses par jour et par modalité, pour la fenêtre donnée."""
    api_key = getattr(settings, "TALLY_API_KEY", "")
    if not api_key:
        raise TallyConfigurationError(
            "TALLY_API_KEY n'est pas configurée : impossible de collecter les réponses Tally."
        )

    points = []
    for form_config in getattr(settings, "TALLY_FORMS", []):
        points.extend(_collect_form(api_key, form_config, start_date, end_date))
    return points


def _collect_form(api_key, form_config, start_date, end_date):
    form_id = form_config["form_id"]
    metric = form_config["metric"]
    scale = form_config["scale"]

    counts = Counter()
    ignored = Counter()

    for payload in _iter_pages(api_key, form_id, start_date):
        question = _find_question(payload.get("questions") or [], form_config)
        if question is None:
            logger.warning(
                "Tally %s : question introuvable dans le formulaire (métrique %s). "
                "La question a-t-elle été renommée ou supprimée ?",
                form_id,
                metric,
            )
            return []

        option_labels = {
            option.get("id"): option.get("text") for option in (question.get("options") or [])
        }

        for submission in payload.get("submissions") or []:
            day = _submission_day(submission)
            if day is None or not (start_date <= day <= end_date):
                continue

            label = _answer_label(_raw_answer(submission, question["id"]), option_labels)
            if label is None:
                continue

            dimension = _label_to_dimension(label, scale)
            if dimension is None:
                ignored[label] += 1
                continue

            counts[(day, dimension)] += 1

    for label, count in ignored.items():
        logger.warning(
            "Tally %s : %s réponse(s) avec une modalité non reconnue pour l'échelle %s : %r. "
            "Vérifier que les modalités du formulaire n'ont pas changé.",
            form_id,
            count,
            scale,
            label,
        )

    return [
        MetricPoint(
            source=SOURCE,
            metric=metric,
            date=day,
            dimension=dimension,
            value=Decimal(count),
            details={"form_id": form_id},
        )
        for (day, dimension), count in sorted(counts.items())
    ]


def _iter_pages(api_key, form_id, start_date):
    """Parcourt les pages de réponses, de la plus récente à la plus ancienne.

    S'arrête dès qu'une page entière est antérieure à la fenêtre demandée : inutile de
    remonter tout l'historique du formulaire à chaque passage du cron.
    """
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }
    )

    for page in range(1, MAX_PAGES + 1):
        response = session.get(
            f"{API_URL}/forms/{form_id}/submissions",
            params={"page": page, "limit": PAGE_SIZE, "filter": "completed"},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()

        yield payload

        submissions = payload.get("submissions") or []
        if not payload.get("hasMore") or not submissions:
            return

        days = [day for day in (_submission_day(item) for item in submissions) if day is not None]
        if days and max(days) < start_date:
            return

        time.sleep(PAUSE_BETWEEN_REQUESTS)

    logger.warning(
        "Tally %s : arrêt après %s pages. La fenêtre demandée est peut-être trop large.",
        form_id,
        MAX_PAGES,
    )


def _find_question(questions, form_config):
    """Retrouve la question portant la note, sans dépendre d'un identifiant codé en dur.

    Priorité à `question_id` s'il est renseigné, sinon on cherche un fragment du libellé,
    sinon on accepte la question si le formulaire n'en contient qu'une.
    """
    question_id = form_config.get("question_id")
    if question_id:
        return next((q for q in questions if q.get("id") == question_id), None)

    fragment = normalize_label(form_config.get("question_contains", ""))
    if fragment:
        matches = [q for q in questions if fragment in normalize_label(q.get("title"))]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            logger.warning(
                "Tally %s : %s questions correspondent au fragment %r, préciser question_id.",
                form_config["form_id"],
                len(matches),
                form_config.get("question_contains"),
            )
            return None

    if len(questions) == 1:
        return questions[0]
    return None


def _raw_answer(submission, question_id):
    for response in submission.get("responses") or []:
        if response.get("questionId") == question_id:
            return response.get("value", response.get("answer"))
    return None


def _answer_label(raw, option_labels):
    """Rend le libellé lisible de la réponse, ou None s'il n'y a rien d'exploitable.

    Tally renvoie un identifiant d'option pour les questions à choix ; on le traduit
    tout de suite, pour que les alertes parlent de « Sans opinion » et non de « opt9 ».
    """
    if raw is None or raw == "" or raw == []:
        return None

    if isinstance(raw, list):
        if len(raw) != 1:
            return None
        raw = raw[0]

    if isinstance(raw, (str, int)) and not isinstance(raw, bool):
        raw = option_labels.get(raw, raw)
    return str(raw)


def _label_to_dimension(label, scale):
    """Traduit un libellé en modalité stockable, ou None s'il ne rentre pas dans l'échelle."""
    if scale == NOTE_1_5:
        try:
            note = int(float(label))
        except (TypeError, ValueError):
            return None
        return str(note) if 1 <= note <= 5 else None

    if scale == ACCORD_5:
        return ACCORD_5_MAPPING.get(normalize_label(label))

    raise TallyConfigurationError(f"Échelle Tally inconnue : {scale!r}")


def _submission_day(submission):
    """Date locale de la réponse, pour que les jours coïncident avec les autres stats."""
    raw = submission.get("submittedAt") or submission.get("createdAt")
    if not raw:
        return None
    try:
        moment = datetime.datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except ValueError:
        logger.warning("Tally : date de réponse illisible (%r), réponse ignorée.", raw)
        return None
    if timezone.is_naive(moment):
        moment = moment.replace(tzinfo=datetime.timezone.utc)
    return timezone.localtime(moment).date()
