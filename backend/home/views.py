from django.contrib.auth import logout
from django.shortcuts import redirect
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
    return redirect("index")
