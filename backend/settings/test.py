from .local import *  # noqa

DJANGO_SETTINGS_MODULE = "backend.settings.test"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
    "stats_db": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
}

# Ensure templates can be found during tests, especially index.html.
if PROJECT_ROOT not in TEMPLATES[0]["DIRS"]:
    TEMPLATES[0]["DIRS"].append(PROJECT_ROOT)

# Disable rate limiting in tests by setting very high limits
THROTTLE_SAFE_RATE = "10000/hour"
THROTTLE_UNSAFE_RATE = "10000/hour"

# ProConnect / OIDC Settings
PROCONNECT_ENABLED = False
SENTRY_ENABLED = False

# Default mock OIDC endpoints to allow instantiating OIDC backends in tests
OIDC_OP_TOKEN_ENDPOINT = "https://example.com/token"
OIDC_OP_USER_ENDPOINT = "https://example.com/userinfo"
OIDC_OP_JWKS_ENDPOINT = "https://example.com/jwks"
OIDC_OP_AUTHORIZATION_ENDPOINT = "https://example.com/auth"
OIDC_OP_LOGOUT_ENDPOINT = "https://example.com/logout"
OIDC_RP_CLIENT_ID = "mock-client"
OIDC_RP_CLIENT_SECRET = "mock-secret"
OIDC_RP_SIGN_ALGO = "RS256"

if "mozilla_django_oidc" in INSTALLED_APPS:
    INSTALLED_APPS.remove("mozilla_django_oidc")

if "anymail" in INSTALLED_APPS:
    INSTALLED_APPS.remove("anymail")

# Authentication and Authorization Overrides for Tests
LOGIN_REQUIRED = False
LOGIN_URL = "/login/"  # Override base setting to avoid reversing missing oidc url

REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
    "rest_framework.permissions.AllowAny",
]

# Register the bypass auth backend in test environment always
AUTHENTICATION_BACKENDS = [
    "backend.bypass_auth.auth.BypassAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
