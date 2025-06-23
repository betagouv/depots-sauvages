import logging

from django.conf import settings
from rest_framework import permissions, serializers

from backend.antispam_timer.timer import FormTimer
from backend.signalements.models import Signalement

logger = logging.getLogger(__name__)


class SignalementSerializer(serializers.ModelSerializer):
    """
    Serializer for Signalement model with timer validation.
    """

    class Meta:
        model = Signalement
        exclude = ["doc_constat", "lettre_info"]

    def validate(self, data):
        request = self.context.get("request")
        if request and request.method not in permissions.SAFE_METHODS:
            logger.debug(f"SignalementSerializer.validate called with method: {request.method}")
            FormTimer.validate_timer(request, settings.TIMER_BASE_NAME)
            logger.debug("Timer validation completed")
        return data
