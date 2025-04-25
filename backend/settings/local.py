import environ

from backend.settings.base import *  # noqa

env = environ.Env()
environ.Env.read_env(PROJECT_ROOT / ".env")

DJANGO_SETTINGS_MODULE = "backend.settings.local"

ENV_NAME = "dev"

SECRET_KEY = env.str("SECRET_KEY", default="ignore-this-BLKAeaEaZ3KS2RDYPHAcciBBSyRGDR8=")

INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS

DEBUG = True

LOGGING["loggers"]["backend.signalements"]["level"] = "DEBUG"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": PROJECT_ROOT / "db.sqlite3",
    }
}

# Security settings for development
ALLOWED_HOSTS = ["*"]

# CORS/CSRF Settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ["http://localhost:5173"]

# Cookie Settings
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = False  # Needed to access the token in JavaScript
SESSION_COOKIE_SAMESITE = "Lax"

# ConvertAPI Settings
CONVERTAPI_SECRET = env.str("CONVERTAPI_SECRET", default="")
CONVERTAPI_TIMEOUT = env.int("CONVERTAPI_TIMEOUT", default=10)  # Timeout in seconds
CONVERTAPI_BASE_URL = env.str("CONVERTAPI_BASE_URL", default="https://v2.convertapi.com")
