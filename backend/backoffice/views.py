from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from backend.backoffice.serializers import BackofficeProcedureSerializer, StaffUserSerializer
from backend.constatations.models import Constatation

User = get_user_model()


class BackofficeProceduresViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = BackofficeProcedureSerializer
    queryset = Constatation.objects.select_related("user", "suivi_procedure").order_by("-id")


class BackofficeStaffViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = StaffUserSerializer
    queryset = User.objects.filter(is_staff=True).order_by("first_name", "last_name", "email")
