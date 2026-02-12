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
    "corsheaders",
    "django_tasks",
    "anymail",
    "python_odt_template",
    "import_export",
    #
    # Project apps
    "backend.throttling",
    "backend.home",
    "backend.signalements",
    "backend.dn",
    "backend.dn_signalements",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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

# Email sending rate limiting
EMAIL_RATE_LIMIT = "10/m"

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

# DN Integration Settings - Démarche Numérique
DN_GRAPHQL_ENDPOINT = "https://demarche.numerique.gouv.fr/api/v2/graphql"
DN_REQUEST_TIMEOUT = 30
DN_MAX_RETRIES = 3

# ProConnect / OIDC / Login Required
LOGIN_URL = "oidc_authentication_init"
LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"
OIDC_STORE_ID_TOKEN = True

LOGIN_REQUIRED = True
