from django.http import Http404
from rest_framework import mixins, permissions, viewsets
from rest_framework.response import Response

from backend.constatations.concurrency import check_optimistic_lock
from backend.constatations.views import get_user_constatations_queryset
from backend.procedures.models import SuiviProcedure
from backend.procedures.serializers import SuiviProcedureSerializer, SuiviProcedureStaffSerializer


class SuiviProcedureViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    lookup_field = "constatation_id"
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SuiviProcedure.objects.filter(
            constatation__in=get_user_constatations_queryset(user)
        )

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_staff:
            return SuiviProcedureStaffSerializer
        return SuiviProcedureSerializer

    def get_object(self):
        """
        Retrieves or automatically creates the SuiviProcedure object for the given constatation.
        """
        constatation_id = self.kwargs.get(self.lookup_field)
        constatation = (
            get_user_constatations_queryset(self.request.user)
            .filter(id=constatation_id)
            .first()
        )
        if not constatation:
            raise Http404(f"Constatation with ID {constatation_id} not found or access denied.")

        creator = (
            getattr(constatation, "created_by", None)
            or getattr(constatation, "user", None)
            or self.request.user
        )
        obj, _ = SuiviProcedure.objects.get_or_create(
            constatation_id=constatation_id,
            defaults={"created_by": creator, "updated_by": self.request.user},
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        conflict_response = check_optimistic_lock(instance, request.data)
        if conflict_response:
            return conflict_response

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        user = self.request.user
        update_kwargs = {"updated_by": user}
        if serializer.instance.created_by is None:
            constat = serializer.instance.constatation
            creator = (
                getattr(constat, "created_by", None)
                or getattr(constat, "user", None)
                or user
            )
            update_kwargs["created_by"] = creator
        serializer.save(**update_kwargs)
