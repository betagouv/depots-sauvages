from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backend.constatations.models import Constatation


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
