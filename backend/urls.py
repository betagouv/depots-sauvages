from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from backend.dn_signalements.views import (
    DNSignalementDocumentDownloadView,
    DNSignalementViewSet,
    ProcessDossierView,
)
from backend.home.views import index_view
from backend.signalements.views import SignalementDocumentDownloadView, SignalementViewSet

# API Routes registration
router = DefaultRouter()
router.register("signalements", SignalementViewSet, basename="signalement")
router.register("dn-signalements", DNSignalementViewSet, basename="dn-signalement")

# Admin Routes
urlpatterns = [path("admin/", admin.site.urls)]

# API Routes
urlpatterns.extend(
    [
        path(
            "api/signalements/<int:pk>/documents/<str:doc_type>/",
            SignalementDocumentDownloadView.as_view(),
            name="signalement-document-download",
        ),
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
        path("api/", include(router.urls)),
    ]
)

# OIDC Routes
if settings.PROCONNECT_ENABLED:
    urlpatterns.append(path("oidc/", include("mozilla_django_oidc.urls")))

# Frontend Routes
# This is a catch-all pattern that serves the compiled frontend.
# It must be placed at the very end of urlpatterns so that it doesn't
# intercept requests intended for other routes like API, Admin, or OIDC.
urlpatterns.append(re_path(r"^(?!admin|api|oidc).*", index_view, name="index"))
