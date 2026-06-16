from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backend.constatations.models import Constatation
from backend.home.seo_metadata import get_seo_data


class RobotsTxtView(TemplateView):
    """
    Serve dynamic robots.txt based on settings.ENV_NAME
    """

    template_name = "robots.txt"
    content_type = "text/plain"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["env_name"] = settings.ENV_NAME
        context["admin_url"] = f"/{settings.ADMIN_URL_NAME.rstrip('/')}/"
        return context


class IndexView(TemplateView):
    """
    Serve Vue Application
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seo_data = get_seo_data(self.request.path) or {}
        context["seo_title"] = (
            seo_data.get("title")
            or "Protect’Envi - Accompagner les collectivités pour mieux lutter contre les dépôts sauvages."
        )
        context["seo_description"] = (
            seo_data.get("desc") or "Signaler un dépôt sauvage avec Protect'Envi."
        )
        return context


index_view = never_cache(IndexView.as_view())


class UserInfoViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        if request.user.is_authenticated:
            return Response(
                {
                    "is_authenticated": True,
                    "proconnect_enabled": settings.PROCONNECT_ENABLED,
                    "first_name": request.user.first_name,
                    "last_name": request.user.last_name,
                    "email": request.user.email,
                    "procedures_count": Constatation.objects.filter(user=request.user).count(),
                    "is_staff": request.user.is_staff,
                }
            )
        return Response(
            {
                "is_authenticated": False,
                "proconnect_enabled": settings.PROCONNECT_ENABLED,
                "is_staff": False,
            }
        )


def logout_view(request):
    """
    Handles user logout.
    If ProConnect is enabled and the user was authenticated via ProConnect,
    it redirects to the ProConnect logout endpoint to ensure the user is logged
    out from the identity provider as well.
    It passes 'id_token_hint' to identifies the user to the IDP and avoid prompt,
    and 'post_logout_redirect_uri' to redirect back to our app after IDP logout.
    """
    id_token = request.session.get("oidc_id_token")
    auth_backend = request.session.get("_auth_user_backend")
    logout(request)
    oidc_logout_endpoint = getattr(settings, "OIDC_OP_LOGOUT_ENDPOINT", None)
    is_proconnect_user = auth_backend == "backend.proconnect.auth.ProConnectOIDCBackend"
    if settings.PROCONNECT_ENABLED and oidc_logout_endpoint and is_proconnect_user:
        params = {
            "post_logout_redirect_uri": request.build_absolute_uri(reverse("index")),
        }
        if id_token:
            params["id_token_hint"] = id_token
        return redirect(f"{oidc_logout_endpoint}?{urlencode(params)}")
    return redirect("index")
