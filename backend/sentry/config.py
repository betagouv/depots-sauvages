from urllib.parse import urlparse

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

IGNORED_ERRORS = [
    "django.http.response.Http404",
    "django.core.exceptions.PermissionDenied",
    "rest_framework.exceptions.NotFound",
    "rest_framework.exceptions.PermissionDenied",
]

SENSITIVE_PARAM_KEYS = {
    "password",
    "token",
    "secret",
    "authorization",
    "cookie",
    "sessionid",
    "csrftoken",
    "api_key",
    "apikey",
}


def sanitize_sensitive_dict(data):
    if not isinstance(data, dict):
        return data
    cleaned = {}
    for key, value in data.items():
        if any(sensitive in str(key).lower() for sensitive in SENSITIVE_PARAM_KEYS):
            cleaned[key] = "[FILTERED]"
        elif isinstance(value, dict):
            cleaned[key] = sanitize_sensitive_dict(value)
        else:
            cleaned[key] = value
    return cleaned


def sentry_before_send(event, hint):
    request_data = event.get("request", {})
    if "headers" in request_data and isinstance(request_data["headers"], dict):
        request_data["headers"] = sanitize_sensitive_dict(request_data["headers"])
    if "cookies" in request_data and isinstance(request_data["cookies"], dict):
        request_data["cookies"] = sanitize_sensitive_dict(request_data["cookies"])
    if "data" in request_data and isinstance(request_data["data"], dict):
        request_data["data"] = sanitize_sensitive_dict(request_data["data"])
    return event


def make_traces_sampler(default_rate=0.1):
    def traces_sampler(sampling_context):
        wsgi_environ = sampling_context.get("wsgi_environ", {})
        path = wsgi_environ.get("PATH_INFO", "")
        if path in ("/robots.txt", "/sitemap.xml") or path.startswith("/static/"):
            return 0.0
        return default_rate

    return traces_sampler


def extract_sentry_origin(dsn):
    if not dsn:
        return None
    try:
        parsed = urlparse(dsn)
        return f"{parsed.scheme}://{parsed.netloc.split('@')[-1]}"
    except Exception:
        return None


def init_sentry(env, env_name, is_debug=False):
    sentry_enabled = env.bool("SENTRY_ENABLED", default=False)
    if not sentry_enabled:
        return None
    dsn = env.str("SENTRY_DSN", default="")
    if not dsn:
        return None
    release = env.str(
        "SENTRY_RELEASE",
        default=env.str("CONTAINER_VERSION", default=env.str("SOURCE_VERSION", default=None)),
    )
    traces_rate = env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.1)
    profiles_rate = env.float("SENTRY_PROFILES_SAMPLE_RATE", default=0.1)
    send_pii = env.bool("SENTRY_SEND_DEFAULT_PII", default=False)
    sentry_sdk.init(
        dsn=dsn,
        integrations=[DjangoIntegration(), RedisIntegration()],
        traces_sampler=make_traces_sampler(traces_rate),
        profiles_sample_rate=profiles_rate,
        send_default_pii=send_pii,
        environment=env_name,
        release=release,
        ignore_errors=IGNORED_ERRORS,
        before_send=sentry_before_send,
        debug=is_debug,
    )
    return extract_sentry_origin(dsn)
