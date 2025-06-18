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
    cache_format = "throttle_%(scope)s_%(ident)s"

    def get_ident(self, request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        remote_addr = request.META.get("REMOTE_ADDR")
        num_proxies = getattr(settings, "REST_FRAMEWORK", {}).get("NUM_PROXIES", None)
        logger.info(
            f"[THROTTLE] get_ident: xff={xff} remote_addr={remote_addr} num_proxies={num_proxies}"
        )
        # Same DRF's logic, but log everything
        if num_proxies is not None:
            if num_proxies == 0 or xff is None:
                return remote_addr
            addrs = xff.split(",")
            client_addr = addrs[-min(num_proxies, len(addrs))]
            return client_addr.strip()
        return "".join(xff.split()) if xff else remote_addr

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        logger.info(
            f"[THROTTLE] get_cache_key: cache_format={self.cache_format} scope={self.scope} ident={ident}"
        )
        if request.user and request.user.is_authenticated:
            return None  # Only throttle unauthenticated requests.
        if self.scope is None or ident is None:
            logger.warning(
                f"[THROTTLE] get_cache_key: scope or ident is None (scope={self.scope}, ident={ident})"
            )
            return None
        return self.cache_format % {"scope": self.scope, "ident": ident}

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
