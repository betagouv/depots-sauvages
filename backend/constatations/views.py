from rest_framework import mixins, viewsets

from backend.procedures.models import SuiviProcedure

from .models import Constatation
from .serializers import ConstatationSerializer


class ConstatationViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Constatation.objects.all()
    serializer_class = ConstatationSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        constatation = serializer.save(user=user)
        SuiviProcedure.objects.create(constatation=constatation)
