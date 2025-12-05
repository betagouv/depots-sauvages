from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from backend.dn_signalements.views import (
    DNSignalementDocumentDownloadView,
    DNSignalementViewSet,
    ProcessDossierView,
)
from backend.home.views import index_view
from backend.signalements.views import SignalementDocumentDownloadView, SignalementViewSet

# API Routes
router = DefaultRouter()
router.register("signalements", SignalementViewSet, basename="signalement")
router.register("dn-signalements", DNSignalementViewSet, basename="dn-signalement")

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^$", index_view, name="index"),
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
    re_path(r"^(?!admin|api).*", TemplateView.as_view(template_name="index.html")),
]
