import logging

from model_utils.models import TimeStampedModel

from backend.signalements.base import AbstractSignalementBase
from backend.signalements.prejudice import PrejudiceMixin

logger = logging.getLogger(__name__)


class Signalement(AbstractSignalementBase, PrejudiceMixin, TimeStampedModel):
    """
    Model for waste deposit reports
    """

    class Meta:
        verbose_name = "signalement"
        verbose_name_plural = "signalements"

    def __str__(self):
        return f"Dépôt à {self.commune} le {self.date_constat}"
