"""Collecteurs d'agrégats journaliers issus des sources externes.

Chaque module expose une fonction `collect(start_date, end_date) -> list[MetricPoint]`.
Un collecteur ne touche jamais à la base : il interroge son API, compte, et rend des
points de mesure. C'est la commande `sync_external_metrics` qui écrit.

Aucune donnée personnelle ne sort d'un collecteur : ni e-mail, ni nom, ni verbatim,
ni identifiant de répondant. Uniquement des effectifs par jour et par modalité.
"""

from backend.stats.collectors.base import MetricPoint

__all__ = ["MetricPoint"]
