from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from backend.backoffice.serializers import BackofficeProcedureSerializer
from backend.constatations.models import Constatation


class BackofficeProceduresViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = BackofficeProcedureSerializer
    queryset = Constatation.objects.select_related("user", "suivi_procedure").order_by("-id")
