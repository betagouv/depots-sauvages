# backend/middleware/real_ip.py

import logging

logger = logging.getLogger(__name__)


class RealIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        real_ip = request.META.get("HTTP_X_REAL_IP")
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if real_ip:
            request.META["REMOTE_ADDR"] = real_ip
        elif x_forwarded_for:
            request.META["REMOTE_ADDR"] = x_forwarded_for.split(",")[0].strip()
        # else REMOTE_ADDR is already set by Django
        logger.info(
            f"Request IP: {request.META.get('REMOTE_ADDR')} | X-Real-Ip: {real_ip} | X-Forwarded-For: {x_forwarded_for}"
        )
        return self.get_response(request)
