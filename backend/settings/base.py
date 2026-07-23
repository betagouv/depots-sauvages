import locale
from pathlib import Path

SETTINGS_DIR = Path(__file__).resolve().parent
BASE_DIR = SETTINGS_DIR.parent  # Backend base directory
PROJECT_ROOT = BASE_DIR.parent

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #
    # Third party apps
    "django_extensions",
    "rest_framework",
    "trackman",
    "drf_spectacular",
    "corsheaders",
    "django_tasks",
    "django_tasks_db",
    "anymail",
    "python_odt_template",
    "csp",
    #
    # Project apps
    "backend.throttling",
    "backend.home",
    "backend.current_user",
    "backend.admin_config",
    "backend.procedures",
    "backend.backoffice",
    "backend.bypass_auth",
    "backend.constatations.apps.ConstatationsConfig",
    "backend.guillotine",
    "backend.faq",
    "backend.seo",
    "backend.site_content",
    "backend.stats",
]

TRACKMAN_DATABASE_ALIAS = "stats_db"


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "backend.seo.middleware.NonProductionNoIndexMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["dist", PROJECT_ROOT / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

# Set French locale for date formatting
try:
    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
except locale.Error:
    pass  # Fallback to system default

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = PROJECT_ROOT / "dist" / "static"
STATICFILES_DIRS = [
    PROJECT_ROOT / "static",
]


# DRF Settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": [
        "backend.throttling.throttles.SafeRateThrottle",
        "backend.throttling.throttles.UnsafeRateThrottle",
    ],
}

# Global rate limits (requests per minute)
THROTTLE_SAFE_RATE = "300/m"
THROTTLE_UNSAFE_RATE = "60/m"

SPECTACULAR_SETTINGS = {
    "TITLE": "Dépôts Sauvages API",
    "DESCRIPTION": "Documentation interactive des API de la plateforme Dépôts Sauvages.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

# Authentication backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Django Tasks Settings
TASKS = {
    "default": {
        "BACKEND": "django_tasks.backends.immediate.ImmediateBackend",
        "QUEUES": ["default", "documents", "emails"],
    },
}
TASKS_LOGGING = {
    "handlers": ["console"],
    "level": "INFO",
}
LOGGING["loggers"]["django_tasks"] = TASKS_LOGGING


# Cache settings - used in particular for rate limiting
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Anymail settings
ANYMAIL = {
    "TEST_MODE": True,
}

# ProConnect / OIDC / Login Required
LOGIN_URL = "oidc_authentication_init"
LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"
OIDC_STORE_ID_TOKEN = True

LOGIN_REQUIRED = True

# Admin configuration
ENABLE_ADMIN = True
ADMIN_URL_NAME = "admin"

# Bypass Auth Configuration
BYPASS_AUTH_ENABLED = False
ENV_NAME = "development"

# Permissions Policy
PERMISSIONS_POLICY = {
    "accelerometer": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "fullscreen": [],
    "geolocation": [],
    "gyroscope": [],
    "microphone": [],
    "payment": [],
    "usb": [],
}
