from urllib.parse import quote_plus

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
        return Response({"is_authenticated": request.user.is_authenticated})


def logout_view(request):
    logout(request)
    if settings.PROCONNECT_ENABLED and getattr(settings, "OIDC_OP_LOGOUT_ENDPOINT", None):
        logout_url = settings.OIDC_OP_LOGOUT_ENDPOINT
        redirect_url = request.build_absolute_uri(reverse("index"))
        return redirect(f"{logout_url}?post_logout_redirect_uri={quote_plus(redirect_url)}")
    return redirect("index")
