import environ

from backend.settings.base import *  # noqa

env = environ.Env()
environ.Env.read_env(PROJECT_ROOT / ".env")

DJANGO_SETTINGS_MODULE = "backend.settings.local"

ENV_NAME = "dev"

SECRET_KEY = env.str("SECRET_KEY", default="ignore-this-BLKAeaEaZ3KS2RDYPHAcciBBSyRGDR8=")

INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS

DEBUG = True

LOGGING["loggers"]["root"]["level"] = "DEBUG"

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

# Email Configuration
EMAIL_BACKEND = env("EMAIL_BACKEND", default="anymail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@example.com")
SERVER_EMAIL = env("SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

# Anymail Brevo settings
ANYMAIL = {
    "BREVO_API_KEY": env("BREVO_API_KEY"),
    "BREVO_SENDER_DOMAIN": env("BREVO_SENDER_DOMAIN"),
}

# Rate limiting
EMAIL_RATE_LIMIT = env("EMAIL_RATE_LIMIT", default="10/m")
SIGNALEMENT_RATE_LIMIT = env("SIGNALEMENT_RATE_LIMIT", default="10/m")

# DS Integration Settings - Démarches Simplifiées
DS_API_TOKEN = env("DS_API_TOKEN", default=None)
