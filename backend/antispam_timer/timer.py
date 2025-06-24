import logging

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from rest_framework import serializers

logger = logging.getLogger(__name__)


class FormTimer:
    """
    Form timer validation for bot detection.
    Requires proper session management for security.
    """

    CACHE_TIMEOUT = 1800  # 30 minutes
    MIN_FORM_TIME = settings.MIN_FORM_TIME

    @classmethod
    def _get_cache_key(cls, request, base_name):
        """
        Generate cache key for timer data.
        """
        if not request.session.session_key:
            raise serializers.ValidationError(
                "Session invalide. Veuillez recharger la page et réessayer."
            )
        return f"timer_{base_name}_{request.session.session_key}"

    @classmethod
    def start_timer(cls, request, base_name):
        """
        Start timer for a form session.
        """
        cache_key = cls._get_cache_key(request, base_name)
        timer_data = {
            "start_time": timezone.now().timestamp(),
            "base_name": base_name,
            "session_id": request.session.session_key,
        }
        cache.set(cache_key, timer_data, cls.CACHE_TIMEOUT)
        logger.debug(f"Started timer for {base_name} form (session: {request.session.session_key})")

    @classmethod
    def validate_timer(cls, request, base_name):
        """
        Validate timer and return timer data.
        """
        cache_key = cls._get_cache_key(request, base_name)
        timer_data = cache.get(cache_key)
        if not timer_data:
            logger.debug(f"No timer data found for {base_name} - starting timer")
            cls.start_timer(request, base_name)
            raise serializers.ValidationError("Session invalide. Veuillez recharger la page.")
        total_time = timezone.now().timestamp() - timer_data["start_time"]
        logger.debug(f"Validating timer: {total_time:.1f}s (required: {cls.MIN_FORM_TIME}s)")
        if total_time < cls.MIN_FORM_TIME:
            logger.debug("Timer validation failed - keeping original timer")
            raise serializers.ValidationError("Délai de réponse invalide. Veuillez réessayer.")
        logger.debug(f"Timer validation passed: {total_time:.1f}s")
        return timer_data
