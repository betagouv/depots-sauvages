import logging

from django.conf import settings
from rest_framework.throttling import AnonRateThrottle

logger = logging.getLogger(__name__)


class EmailRateThrottle(AnonRateThrottle):
    """
    Custom throttle for email sending endpoint.
    """

    rate = getattr(settings, "EMAIL_RATE_LIMIT")

    def allow_request(self, request, view):
        self.key = self.get_cache_key(request, view)
        self.history = self.cache.get(self.key, []) if self.key else None
        remote_addr = request.META.get("REMOTE_ADDR")
        allowed = super().allow_request(request, view)
        logger.info(
            f"[THROTTLE] key={self.key} rate={self.rate} history={self.history} allowed={allowed} REMOTE_ADDR={remote_addr}"
        )
        return allowed

    def throttle_failure(self):
        logger.warning(f"[THROTTLE] Request throttled for key={self.key} rate={self.rate}")
        return super().throttle_failure()
