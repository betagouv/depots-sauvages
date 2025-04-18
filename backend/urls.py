from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from backend.home.views import index_view
from backend.signalements.views import SignalementDocumentDownloadView, SignalementViewSet

# API Routes
router = DefaultRouter()
router.register("signalements", SignalementViewSet, basename="signalement")

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^$", index_view, name="index"),
    path("api/", include(router.urls)),
    # Document download outside the API namespace
    path(
        "documents/signalements/<int:pk>/",
        SignalementDocumentDownloadView.as_view(),
        name="signalement-document",
    ),
]
