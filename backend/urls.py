from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from backend.email_sending.views import SendEmailViewSet
from backend.home.views import index_view
from backend.signalements.views import SignalementDocumentDownloadView, SignalementViewSet

# API router
router = DefaultRouter()
router.register("signalements", SignalementViewSet, basename="signalement")

urlpatterns = [
    # Admin routes
    path("admin/", admin.site.urls),
    # Vue router routes
    re_path(r"^$", index_view, name="index"),
    path("debuter-procedure/", index_view, name="debuter-procedure"),
    path("accompagnement/", index_view, name="accompagnement"),
    # API routes
    path("api/", include(router.urls)),
    path(
        "api/signalements/<int:pk>/documents/<str:doc_type>/",
        SignalementDocumentDownloadView.as_view(),
        name="signalement-document-download",
    ),
    path(
        "api/signalements/<int:pk>/send-email/",
        SendEmailViewSet.as_view({"post": "send_email"}),
        name="signalement-send-email",
    ),
]
