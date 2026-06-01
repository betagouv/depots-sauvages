from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework import mixins, permissions, viewsets

from backend.signalements.views import SignalementDocumentDownloadViewMixin

from .models import Constatation
from .serializers import ConstatationSerializer


class ConstatationViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ConstatationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Constatation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@method_decorator(login_required, name="dispatch")
class ConstatationDocumentDownloadView(SignalementDocumentDownloadViewMixin):
    """
    Download documents for Constatation instances securely.
    """

    model_class = Constatation

    def _get_signalement(self, pk):
        return get_object_or_404(self.model_class, pk=pk, user=self.request.user)
