# On Scalingo, REMOTE_ADDR is set to the real client IP via X-Forwarded-For
# by the platform's proxy. There is a header X-Real-IP that is set to the
# real client IP, but by default it is not used by Django and DRF and we
# don't need to use it.

from django.conf import settings
from rest_framework.throttling import AnonRateThrottle


class EmailRateThrottle(AnonRateThrottle):
    """
    Custom throttle for email sending endpoint.
    """

    rate = getattr(settings, "EMAIL_RATE_LIMIT")

    def get_cache_key(self, request, view):
        """
        Get the cache key for the request based on the IP address in
        the REMOTE_ADDR header. We override the default implementation
        it uses scope and ident as the cache key, and these were not
        working as expected.
        """
        client_ip = request.META.get("REMOTE_ADDR")
        if not client_ip:
            return None
        return f"email_throttle_{client_ip}"
