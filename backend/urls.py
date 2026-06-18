from csp.decorators import csp_update
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from backend.bypass_auth.views import BypassAuthConfigView, BypassAuthLoginView
from backend.constatations.views import ConstatationDocumentDownloadView, ConstatationViewSet
from backend.dn_signalements.views import (
    DNSignalementDocumentDownloadView,
    ProcessDossierView,
    SyncUserSignalementsView,
)
from backend.faq.views import FAQItemViewSet
from backend.home.views import UserInfoViewSet, index_view, logout_view
from backend.seo.views import RobotsTxtView
from backend.procedures.views import SuiviProcedureViewSet

# API Routes registration
router = DefaultRouter()
router.register("user-info", UserInfoViewSet, basename="user-info")
router.register("suivi-procedure", SuiviProcedureViewSet, basename="suivi-procedure")
router.register("constatations", ConstatationViewSet, basename="constatation")
router.register("faq-items", FAQItemViewSet, basename="faq-item")


# Admin Routes
if settings.ENABLE_ADMIN:
    urlpatterns = [path(f"{settings.ADMIN_URL_NAME}/", admin.site.urls)]
else:
    urlpatterns = []

# API Routes
urlpatterns.extend(
    [
        path(
            "api/constatations/<int:pk>/documents/<str:doc_type>/",
            ConstatationDocumentDownloadView.as_view(),
            name="constatation-document-download",
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
        path(
            "api/dossiers/sync/",
            SyncUserSignalementsView.as_view(),
            name="dossiers-sync",
        ),
        path(
            "api/bypass-auth/config/",
            BypassAuthConfigView.as_view(),
            name="bypass-auth-config",
        ),
        path(
            "api/bypass-auth/login/",
            BypassAuthLoginView.as_view(),
            name="bypass-auth-login",
        ),
        path("api/", include(router.urls)),
        path("logout/", logout_view, name="logout"),
    ]
)

# API Schema & Documentation
if settings.DEBUG and settings.ENV_NAME == "dev":
    urlpatterns.extend(
        [
            path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
            path(
                "api/swagger/",
                csp_update(
                    {
                        "style-src": ["https://cdn.jsdelivr.net"],
                        "script-src": ["https://cdn.jsdelivr.net", "'unsafe-inline'"],
                        "img-src": ["https://cdn.jsdelivr.net"],
                    }
                )(SpectacularSwaggerView.as_view(url_name="schema")),
                name="swagger-ui",
            ),
        ]
    )


# OIDC Routes
if settings.PROCONNECT_ENABLED:
    urlpatterns.append(path("oidc/", include("mozilla_django_oidc.urls")))

# Protected Frontend Routes
urlpatterns.append(
    re_path(
        r"^signalements-dn/(?P<dossier_id>\d+)/?$",
        RedirectView.as_view(url="/suivi-procedure/%(dossier_id)s/", permanent=True),
    )
)


# Sentry Debug
if getattr(settings, "SENTRY_DEBUG", False):

    def trigger_error(request):
        division_by_zero = 1 / 0  # noqa

    urlpatterns.append(path("sentry-debug/", trigger_error))


# Robots.txt Route
urlpatterns.append(path("robots.txt", RobotsTxtView.as_view(), name="robots_txt"))

# Frontend Routes
# This is a catch-all pattern that serves the compiled frontend.
# It must be placed at the very end of urlpatterns so that it doesn't
# intercept requests intended for other routes like API, Admin, or OIDC.
admin_url = settings.ADMIN_URL_NAME.rstrip("/")
urlpatterns.append(
    re_path(r"^(?!%s|api|oidc|sentry-debug|robots\.txt).*" % admin_url, index_view, name="index")
)
