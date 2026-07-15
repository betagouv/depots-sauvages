from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseBypassAuthView(APIView):
    """
    Base view for bypass authentication that ensures the feature
    is enabled in settings before executing any request.
    """

    def dispatch(self, request, *args, **kwargs):
        if not getattr(settings, "BYPASS_AUTH_ENABLED", False):
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class BypassAuthConfigView(BaseBypassAuthView):
    """
    Returns whether bypass auth is enabled in settings.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        enabled = getattr(settings, "BYPASS_AUTH_ENABLED", False)
        return Response({"enabled": enabled})


class BypassAuthLoginView(BaseBypassAuthView):
    """
    Logs in the requested user without credentials by utilizing the
    custom BypassAuthBackend.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "email is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, email=email)
        if not user:
            return Response(
                {"error": "Adresse électronique inconnue ou non autorisée."},
                status=status.HTTP_403_FORBIDDEN,
            )
        login(request, user)
        return Response(
            {
                "message": "Successfully logged in via bypass",
                "user": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                },
            }
        )
