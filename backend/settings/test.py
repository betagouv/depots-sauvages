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

# DS Integration Settings for tests
DS_API_TOKEN = "test-token"
DS_SIGNALEMENT_DEMARCHE_ID = "test-demarche-id"
