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

# DN Integration Settings - Démarche Numérique
DN_GRAPHQL_ENDPOINT = env.str(
    "DN_GRAPHQL_ENDPOINT", default="https://demarche.numerique.gouv.fr/api/v2/graphql"
)
DN_API_TOKEN = env("DN_API_TOKEN", default="")
DN_DEMARCHE_NUMBER = env.int("DN_DEMARCHE_NUMBER", default=0)

# ProConnect / OIDC Settings
PROCONNECT_ENABLED = env.bool("VITE_PROCONNECT_ENABLED", default=False)

if PROCONNECT_ENABLED:
    INSTALLED_APPS += ["mozilla_django_oidc"]
    AUTHENTICATION_BACKENDS = [
        "backend.home.auth.ProConnectOIDCBackend",
        "django.contrib.auth.backends.ModelBackend",
    ]
    OIDC_RP_CLIENT_ID = env("OIDC_RP_CLIENT_ID")
    OIDC_RP_CLIENT_SECRET = env("OIDC_RP_CLIENT_SECRET")
    OIDC_OP_AUTHORIZATION_ENDPOINT = env("OIDC_OP_AUTHORIZATION_ENDPOINT")
    OIDC_OP_TOKEN_ENDPOINT = env("OIDC_OP_TOKEN_ENDPOINT")
    OIDC_OP_USER_ENDPOINT = env("OIDC_OP_USER_ENDPOINT")
    OIDC_OP_JWKS_ENDPOINT = env("OIDC_OP_JWKS_ENDPOINT")
    OIDC_OP_LOGOUT_ENDPOINT = env("OIDC_OP_LOGOUT_ENDPOINT", default="")
    OIDC_RP_SIGN_ALGO = "RS256"


# Auth Configuration
LOGIN_REQUIRED = env.bool("LOGIN_REQUIRED", default=False)

if not LOGIN_REQUIRED:
    REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
        "rest_framework.permissions.AllowAny",
    ]
