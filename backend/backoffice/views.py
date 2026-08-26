from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from backend.backoffice.filters import BackofficeProcedureFilterSet
from backend.backoffice.serializers import BackofficeProcedureSerializer, StaffUserSerializer
from backend.backoffice.stats import get_backoffice_dashboard_stats
from backend.constatations.models import Constatation

User = get_user_model()


class BackofficePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 200


class BackofficeProceduresViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = BackofficeProcedureSerializer
    pagination_class = BackofficePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BackofficeProcedureFilterSet
    queryset = (
        Constatation.objects.defer("doc_constat", "lettre_info")
        .select_related("user", "suivi_procedure")
        .order_by("-id")
    )


class BackofficeDashboardStatsViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def list(self, request):
        return Response(get_backoffice_dashboard_stats())


class BackofficeStaffViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = StaffUserSerializer
    queryset = User.objects.filter(is_staff=True).order_by("first_name", "last_name", "email")
