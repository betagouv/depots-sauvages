# On Scalingo, REMOTE_ADDR is set to the real client IP via X-Forwarded-For
# by the platform's proxy. There is a header X-Real-IP that is set to the
# real client IP, but by default it is not used by Django and DRF and we
# don't need to use it.

from django.conf import settings
from rest_framework.permissions import SAFE_METHODS
from rest_framework.throttling import AnonRateThrottle


class BaseRateThrottle(AnonRateThrottle):
    """
    Base throttle class with common functionality for IP-based rate limiting.
    """

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
        return f"{self.cache_key_prefix}_{client_ip}"


class EmailRateThrottle(BaseRateThrottle):
    """
    Custom throttle for email sending endpoint.
    """

    rate = getattr(settings, "EMAIL_RATE_LIMIT")
    cache_key_prefix = "email_throttle"


class SafeRateThrottle(BaseRateThrottle):
    """
    Throttle class for read-only requests (GET, HEAD, OPTIONS).
    """

    rate = getattr(settings, "THROTTLE_SAFE_RATE", "300/m")
    cache_key_prefix = "safe_throttle"

    def allow_request(self, request, view):
        if request.method not in SAFE_METHODS:
            return True
        return super().allow_request(request, view)


class UnsafeRateThrottle(BaseRateThrottle):
    """
    Throttle class for write requests (POST, PUT, PATCH, DELETE).
    """

    rate = getattr(settings, "THROTTLE_UNSAFE_RATE", "60/m")
    cache_key_prefix = "unsafe_throttle"

    def allow_request(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return super().allow_request(request, view)
