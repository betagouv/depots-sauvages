import csv
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from backend.backoffice.filters import BackofficeProcedureFilterSet, BackofficeUserFilterSet
from backend.backoffice.serializers import (
    BackofficeProcedureSerializer,
    BackofficeUserSerializer,
    StaffUserSerializer,
)
from backend.backoffice.stats import get_backoffice_dashboard_stats
from backend.constatations.models import Constatation

User = get_user_model()


class BackofficePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 200


class BackofficeUsersPagination(PageNumberPagination):
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
        Constatation.objects.defer("doc_constat", "lettre_info", "photos")
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


class BackofficeUsersViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = BackofficeUserSerializer
    pagination_class = BackofficeUsersPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BackofficeUserFilterSet

    def get_queryset(self):
        return (
            User.objects.annotate(procedures_count=Count("constatations"))
            .select_related("proconnect_profile")
            .order_by("-id")
        )

    @action(detail=False, methods=["get"], url_path="export-csv")
    def export_csv(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
        response["Content-Disposition"] = 'attachment; filename="utilisateurs.csv"'

        writer = csv.writer(response, delimiter=";")
        writer.writerow(
            [
                "Identifiant",
                "E-mail",
                "Prénom",
                "Nom",
                "Est équipe / staff",
                "Profil ProConnect lié",
                "SIRET ProConnect",
                "SIREN ProConnect",
                "Organisation ProConnect",
                "Rôles ProConnect",
                "Nombre de procédures",
                "Date de création",
                "Dernière connexion",
            ]
        )

        for user in queryset:
            profile = getattr(user, "proconnect_profile", None)
            has_pc = "Oui" if profile else "Non"
            siret = profile.siret if profile else ""
            siren = profile.siren if profile else ""
            org = profile.organization_label if profile else ""
            roles = ", ".join(profile.roles) if profile and profile.roles else ""
            date_joined = user.date_joined.strftime("%Y-%m-%d %H:%M:%S") if user.date_joined else ""
            last_login = user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else ""

            writer.writerow(
                [
                    user.id,
                    user.email,
                    user.first_name,
                    user.last_name,
                    "Oui" if user.is_staff else "Non",
                    has_pc,
                    siret,
                    siren,
                    org,
                    roles,
                    user.procedures_count,
                    date_joined,
                    last_login,
                ]
            )

        return response
