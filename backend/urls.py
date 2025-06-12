from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from backend.email_sending.views import SendEmailViewSet
from backend.home.views import index_view
from backend.signalements.views import SignalementDocumentDownloadView, SignalementViewSet

# API Routes
router = DefaultRouter()
router.register("signalements", SignalementViewSet, basename="signalement")

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^$", index_view, name="index"),
    path("api/", include(router.urls)),
    path(
        "api/signalements/<int:pk>/documents/<str:doc_type>/",
        SignalementDocumentDownloadView.as_view(),
        name="signalement-document-download",
    ),
    path(
        "api/signalements/<int:pk>/send-email/",
        SendEmailViewSet.as_view({"post": "send_signalement"}),
        name="signalement-send-email",
    ),
    re_path(r"^(?!admin|api).*", TemplateView.as_view(template_name="index.html")),
]
