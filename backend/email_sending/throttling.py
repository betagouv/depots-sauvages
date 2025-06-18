import logging

from django.conf import settings
from rest_framework.throttling import AnonRateThrottle

logger = logging.getLogger(__name__)


class EmailRateThrottle(AnonRateThrottle):
    """
    Custom throttle for email sending endpoint.
    """

    scope = "email"
    rate = getattr(settings, "EMAIL_RATE_LIMIT")

    def get_cache_key(self, request, view):
        # Always use REMOTE_ADDR as the identifier
        ident = request.META.get("REMOTE_ADDR")
        logger.info(f"[THROTTLE] get_cache_key: scope={self.scope} ident={ident}")
        if not ident:
            logger.warning("[THROTTLE] No REMOTE_ADDR found, cannot throttle.")
            return None
        return f"throttle_{self.scope}_{ident}"

    def allow_request(self, request, view):
        self.key = self.get_cache_key(request, view)
        self.history = self.cache.get(self.key, []) if self.key else None
        allowed = super().allow_request(request, view)
        logger.info(
            f"[THROTTLE] key={self.key} rate={self.rate} history={self.history} allowed={allowed} REMOTE_ADDR={request.META.get('REMOTE_ADDR')}"
        )
        return allowed

    def throttle_failure(self):
        logger.warning(f"[THROTTLE] Request throttled for key={self.key} rate={self.rate}")
        return super().throttle_failure()
