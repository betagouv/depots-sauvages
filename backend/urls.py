from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from backend.ds_signalements.views import (
    DSSignalementDocumentDownloadView,
    DSSignalementViewSet,
    ProcessDossierView,
)
from backend.home.views import index_view
from backend.signalements.views import SignalementDocumentDownloadView, SignalementViewSet

# API Routes
router = DefaultRouter()
router.register("signalements", SignalementViewSet, basename="signalement")
router.register("ds-signalements", DSSignalementViewSet, basename="ds-signalement")

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^$", index_view, name="index"),
    path(
        "api/signalements/<int:pk>/documents/<str:doc_type>/",
        SignalementDocumentDownloadView.as_view(),
        name="signalement-document-download",
    ),
    path(
        "api/ds-signalements/<int:pk>/documents/<str:doc_type>/",
        DSSignalementDocumentDownloadView.as_view(),
        name="ds-signalement-document-download",
    ),
    path(
        "api/signalements/process-ds-dossier/",
        ProcessDossierView.as_view(),
        name="signalements-process-ds-dossier",
    ),
    path("api/", include(router.urls)),
    re_path(r"^(?!admin|api).*", TemplateView.as_view(template_name="index.html")),
]
