import environ

from backend.settings.base import *  # noqa

env = environ.Env()

ENV_NAME = env("ENV_NAME")

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=False)

LOGGING_LEVEL = env("LOGGING_LEVEL", default="INFO")

LOGGING["loggers"]["backend.signalements"] = {
    "handlers": ["console"],
    "level": LOGGING_LEVEL,
    "propagate": True,
}

DATABASES = {
    "default": env.db("DATABASE_URL", default=f"file:///{PROJECT_ROOT / 'db.sqlite3'}"),
}
# Security settings for production
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])


# CORS/CSRF Settings
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Cookie Settings
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = False  # Needed to access the token in JavaScript
SESSION_COOKIE_SAMESITE = "Lax"

# Django Tasks Settings
TASKS["default"]["BACKEND"] = "django_tasks.backends.database.DatabaseBackend"

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

# DN Integration Settings - Démarche Numérique
DN_GRAPHQL_ENDPOINT = env.str(
    "DN_GRAPHQL_ENDPOINT", default="https://demarche.numerique.gouv.fr/api/v2/graphql"
)
DN_API_TOKEN = env("DN_API_TOKEN", default=None)
DN_REQUEST_TIMEOUT = env.int("DN_REQUEST_TIMEOUT", default=30)
DN_MAX_RETRIES = env.int("DN_MAX_RETRIES", default=3)

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
