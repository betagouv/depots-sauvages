import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from backend.settings.base import *  # noqa

env = environ.Env()

ENV_NAME = env("ENV_NAME")

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=False)
SENTRY_DEBUG = env.bool("SENTRY_DEBUG", default=False)
SENTRY_ENABLED = env.bool("SENTRY_ENABLED", default=False)

if SENTRY_ENABLED:
    sentry_sdk.init(
        dsn=env("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.1),
        profiles_sample_rate=env.float("SENTRY_PROFILES_SAMPLE_RATE", default=0.1),
        send_default_pii=env.bool("SENTRY_SEND_DEFAULT_PII", default=False),
        environment=ENV_NAME,
    )


LOGGING_LEVEL = env("LOGGING_LEVEL", default="INFO")

LOGGING["loggers"]["backend.constatations"] = {
    "handlers": ["console"],
    "level": LOGGING_LEVEL,
    "propagate": True,
}

DATABASES = {
    "default": env.db("DATABASE_URL", default=f"file:///{PROJECT_ROOT / 'db.sqlite3'}"),
}

# Security settings for production
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
SECURE_BROWSER_XSS_FILTER = env.bool("SECURE_BROWSER_XSS_FILTER", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("SECURE_CONTENT_TYPE_NOSNIFF", default=True)

# External services domains used in CSP
STATS_BETA_GOUV = "https://stats.beta.gouv.fr"
TALLY_SO = "https://tally.so"
CRISP_CLIENT = "https://client.crisp.chat"
CRISP_IMAGE = "https://image.crisp.chat"
CRISP_WSS = "wss://client.relay.crisp.chat"
GRIST = "https://grist.numerique.gouv.fr"
ICONIFY = "https://api.iconify.design"
API_ADRESSE_DATA_GOUV = "https://api-adresse.data.gouv.fr"
RECHERCHE_ENTREPRISES_API = "https://recherche-entreprises.api.gouv.fr"

# Content Security Policy (django-csp 4.0+)
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": env.list("CSP_DEFAULT_SRC", default=["'self'"]),
        "script-src": env.list(
            "CSP_SCRIPT_SRC",
            default=[
                "'self'",
                STATS_BETA_GOUV,
                TALLY_SO,
                CRISP_CLIENT,
            ],
        ),
        "style-src": env.list("CSP_STYLE_SRC", default=["'self'", "'unsafe-inline'", CRISP_CLIENT]),
        "img-src": env.list(
            "CSP_IMG_SRC",
            default=[
                "'self'",
                "data:",
                STATS_BETA_GOUV,
                TALLY_SO,
                CRISP_CLIENT,
                CRISP_IMAGE,
            ],
        ),
        "font-src": env.list("CSP_FONT_SRC", default=["'self'", "data:", CRISP_CLIENT]),
        "frame-src": env.list("CSP_FRAME_SRC", default=["'self'", TALLY_SO, GRIST]),
        "media-src": env.list("CSP_MEDIA_SRC", default=["'self'", CRISP_CLIENT]),
        "connect-src": env.list(
            "CSP_CONNECT_SRC",
            default=[
                "'self'",
                STATS_BETA_GOUV,
                CRISP_CLIENT,
                CRISP_WSS,
                ICONIFY,
                API_ADRESSE_DATA_GOUV,
                RECHERCHE_ENTREPRISES_API,
            ],
        ),
    }
}


# CORS/CSRF Settings
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Cookie Settings
CSRF_COOKIE_NAME = "__Host-csrftoken"
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = False  # Needed to access the token in JavaScript
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Django Tasks Settings
TASKS["default"]["BACKEND"] = "django_tasks_db.DatabaseBackend"

# Email Configuration
EMAIL_BACKEND = env("EMAIL_BACKEND", default="anymail.backends.brevo.EmailBackend")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = env("SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

# Anymail settings for production
ANYMAIL = {
    "TEST_MODE": False,
    "BREVO_API_KEY": env("BREVO_API_KEY"),
    "BREVO_SENDER_DOMAIN": env("BREVO_SENDER_DOMAIN"),
}

# Rate limiting
EMAIL_RATE_LIMIT = env("EMAIL_RATE_LIMIT", default="10/hour")
SIGNALEMENT_RATE_LIMIT = env("SIGNALEMENT_RATE_LIMIT", default="10/hour")

# Reverse proxy settings
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# If Redis is available, use it, notably for shared throttling state.
redis_url = env("REDIS_URL", default=None)
if redis_url:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": redis_url,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }

# ProConnect / OIDC Settings
PROCONNECT_ENABLED = env.bool("VITE_PROCONNECT_ENABLED", default=False)

if PROCONNECT_ENABLED:
    INSTALLED_APPS += ["mozilla_django_oidc"]
    AUTHENTICATION_BACKENDS = [
        "backend.proconnect.auth.ProConnectOIDCBackend",
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
    OIDC_RP_SCOPES = "openid email given_name usual_name"


# Auth Configuration
LOGIN_REQUIRED = env.bool("VITE_LOGIN_REQUIRED", default=True)

# Admin configuration
ENABLE_ADMIN = env.bool("ENABLE_ADMIN", default=True)
ADMIN_URL_NAME = env.str("ADMIN_URL_NAME", default="admin")

if not LOGIN_REQUIRED:
    REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
        "rest_framework.permissions.AllowAny",
    ]

# Bypass Auth in Demo Mode - strictly forbidden in production
BYPASS_AUTH_ENABLED = env.bool("BYPASS_AUTH_ENABLED", default=False)
if "prod" in ENV_NAME:
    BYPASS_AUTH_ENABLED = False

if BYPASS_AUTH_ENABLED:
    AUTHENTICATION_BACKENDS.insert(0, "backend.bypass_auth.auth.BypassAuthBackend")
