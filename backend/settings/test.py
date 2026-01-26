from .local import *  # noqa

DJANGO_SETTINGS_MODULE = "backend.settings.test"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
}

# Disable rate limiting in tests by setting very high limits
SIGNALEMENT_RATE_LIMIT = "100/hour"
EMAIL_RATE_LIMIT = "100/hour"

# DN Integration Settings for tests
DN_GRAPHQL_ENDPOINT = "https://demarche.numerique.gouv.fr/api/v2/graphql"
DN_API_TOKEN = "test-token"

# ProConnect / OIDC Settings
PROCONNECT_ENABLED = False

if "mozilla_django_oidc" in INSTALLED_APPS:
    INSTALLED_APPS.remove("mozilla_django_oidc")

if "anymail" in INSTALLED_APPS:
    INSTALLED_APPS.remove("anymail")

LOGIN_REQUIRED = False
PROCONNECT_ENABLED = False
LOGIN_URL = "/login/"  # Override base setting to avoid reversing missing oidc url
