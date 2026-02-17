from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from backend.dn_signalements.views import (
    DNSignalementDocumentDownloadView,
    DNSignalementViewSet,
    ProcessDossierView,
    UserDossiersView,
)
from backend.home.views import UserInfoViewSet, index_view, logout_view

# API Routes registration
router = DefaultRouter()
router.register("dn-signalements", DNSignalementViewSet, basename="dn-signalement")
router.register("user-info", UserInfoViewSet, basename="user-info")

# Admin Routes
urlpatterns = [path("admin/", admin.site.urls)]

# API Routes
urlpatterns.extend(
    [
        path(
            "api/dn-signalements/<int:pk>/documents/<str:doc_type>/",
            DNSignalementDocumentDownloadView.as_view(),
            name="dn-signalement-document-download",
        ),
        path(
            "api/signalements/process-dn-dossier/",
            ProcessDossierView.as_view(),
            name="signalements-process-dn-dossier",
        ),
        path(
            "api/my-dossiers/",
            UserDossiersView.as_view(),
            name="user-dossiers",
        ),
        path("api/", include(router.urls)),
        path("logout/", logout_view, name="logout"),
    ]
)

# OIDC Routes
if settings.PROCONNECT_ENABLED:
    urlpatterns.append(path("oidc/", include("mozilla_django_oidc.urls")))

# Protected Frontend Routes
if settings.LOGIN_REQUIRED:
    urlpatterns.append(re_path(r"^signalements-dn/.*", login_required(index_view)))
    urlpatterns.append(re_path(r"^mes-dossiers/?$", login_required(index_view)))
else:
    urlpatterns.append(re_path(r"^signalements-dn/.*", index_view))

# Sentry Debug
if getattr(settings, "SENTRY_DEBUG", False):

    def trigger_error(request):
        division_by_zero = 1 / 0  # noqa

    urlpatterns.append(path("sentry-debug/", trigger_error))


# Frontend Routes
# This is a catch-all pattern that serves the compiled frontend.
# It must be placed at the very end of urlpatterns so that it doesn't
# intercept requests intended for other routes like API, Admin, or OIDC.
urlpatterns.append(re_path(r"^(?!admin|api|oidc|sentry-debug).*", index_view, name="index"))
