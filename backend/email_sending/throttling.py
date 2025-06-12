from django.conf import settings
from rest_framework.throttling import AnonRateThrottle


class EmailRateThrottle(AnonRateThrottle):
    """
    Custom throttle for email sending endpoint.
    """

    rate = getattr(settings, "EMAIL_RATE_LIMIT")
