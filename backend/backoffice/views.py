from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
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


class BackofficeDashboardStatsViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def list(self, request):
        real_procedures = Constatation.objects.exclude(ceci_est_un_test=True)

        total_active = real_procedures.filter(
            suivi_procedure__etape_en_cours__lt=5, suivi_procedure__dossier_archive=False
        ).count()

        ar_waiting = real_procedures.filter(
            suivi_procedure__etape_en_cours__lt=5,
            suivi_procedure__lettre_envoyee=True,
            suivi_procedure__ar_recu=False,
        ).count()

        decision_to_take = real_procedures.filter(suivi_procedure__etape_en_cours=3).count()

        now = timezone.now()
        closed_this_month = real_procedures.filter(
            Q(suivi_procedure__etape_en_cours=5) | Q(suivi_procedure__dossier_archive=True),
            suivi_procedure__modified__year=now.year,
            suivi_procedure__modified__month=now.month,
        ).count()

        return Response(
            {
                "totalActive": total_active,
                "actionRequired": 0,
                "arWaiting": ar_waiting,
                "decisionToTake": decision_to_take,
                "closedThisMonth": closed_this_month,
            }
        )


class BackofficeStaffViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = StaffUserSerializer
    queryset = User.objects.filter(is_staff=True).order_by("first_name", "last_name", "email")
