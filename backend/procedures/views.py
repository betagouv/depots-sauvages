from rest_framework import viewsets, mixins, permissions
from backend.procedures.models import SuiviProcedure
from backend.procedures.serializers import SuiviProcedureSerializer


class SuiviProcedureViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = SuiviProcedure.objects.all()
    serializer_class = SuiviProcedureSerializer
    lookup_field = "signalement_id"
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieves or automatically creates the SuiviProcedure object for the given signalement.
        """
        signalement_id = self.kwargs.get(self.lookup_field)
        # Ensure the procedure tracking exists as soon as we try to access it
        obj, created = SuiviProcedure.objects.get_or_create(signalement_id=signalement_id)
        return obj
