import datetime
import unicodedata
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True)
class MetricPoint:
    """Un agrégat : un jour, une métrique, une modalité, un effectif."""

    source: str
    metric: str
    date: datetime.date
    dimension: str
    value: Decimal
    details: dict = field(default_factory=dict)


def normalize_label(label):
    """Réduit un libellé à sa forme comparable : sans accents, sans casse, sans ponctuation.

    « Tout à fait d'accord » et « TOUT A FAIT D'ACCORD  » donnent la même clé, ce qui
    évite qu'une correction de typo dans Tally fasse disparaître les données.
    """
    if label is None:
        return ""
    decomposed = unicodedata.normalize("NFKD", str(label))
    without_accents = "".join(char for char in decomposed if not unicodedata.combining(char))
    return "".join(char for char in without_accents.lower() if char.isalnum())
