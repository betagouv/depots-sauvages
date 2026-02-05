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


class IndexView(TemplateView):
    """
    Serve Vue Application
    """

    template_name = "index.html"


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
                    "email": request.user.username,
                }
            )
        return Response(
            {
                "is_authenticated": False,
                "proconnect_enabled": settings.PROCONNECT_ENABLED,
            }
        )


def logout_view(request):
    """
    Handles user logout.
    If ProConnect is enabled, it redirects to the ProConnect logout endpoint
    to ensure the user is logged out from the identity provider as well.
    It passes 'id_token_hint' to identifies the user to the IDP and avoid prompt,
    and 'post_logout_redirect_uri' to redirect back to our app after IDP logout.
    """
    id_token = request.session.get("oidc_id_token")
    logout(request)
    oidc_logout_endpoint = getattr(settings, "OIDC_OP_LOGOUT_ENDPOINT", None)
    if settings.PROCONNECT_ENABLED and oidc_logout_endpoint:
        params = {
            "post_logout_redirect_uri": request.build_absolute_uri(reverse("index")),
        }
        if id_token:
            params["id_token_hint"] = id_token
        return redirect(f"{oidc_logout_endpoint}?{urlencode(params)}")
    return redirect("index")
