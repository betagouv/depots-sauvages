from django.http import Http404
from rest_framework import mixins, permissions, viewsets

from backend.constatations.models import Constatation
from backend.procedures.models import SuiviProcedure
from backend.procedures.serializers import SuiviProcedureSerializer, SuiviProcedureStaffSerializer


class SuiviProcedureViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = SuiviProcedure.objects.all()
    lookup_field = "constatation_id"
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_staff:
            return SuiviProcedureStaffSerializer
        return SuiviProcedureSerializer

    def get_object(self):
        """
        Retrieves or automatically creates the SuiviProcedure object for the given constatation.
        """
        constatation_id = self.kwargs.get(self.lookup_field)
        # Staff members can access the procedure for any Constatation, whereas regular
        # users can only access it for Constatations they created.
        if self.request.user.is_staff:
            if not Constatation.objects.filter(id=constatation_id).exists():
                raise Http404(f"Constatation with ID {constatation_id} not found.")
        else:
            if not Constatation.objects.filter(id=constatation_id, user=self.request.user).exists():
                raise Http404(f"Constatation with ID {constatation_id} not found or access denied.")
        # Ensure the procedure tracking exists as soon as we try to access it
        obj, created = SuiviProcedure.objects.get_or_create(constatation_id=constatation_id)
        return obj
