# backend/middleware/real_ip.py

import logging

logger = logging.getLogger(__name__)


class RealIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            # Use the first IP in the list (the real client)
            request.META["REMOTE_ADDR"] = x_forwarded_for.split(",")[0].strip()
        else:
            real_ip = request.META.get("REMOTE_ADDR")
        logger.info(
            f"Request IP: {real_ip} | X-Forwarded-For: {x_forwarded_for} | REMOTE_ADDR: {request.META.get('REMOTE_ADDR')}"
        )
        return self.get_response(request)
