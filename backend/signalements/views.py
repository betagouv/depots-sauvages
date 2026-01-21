from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from backend.signalements.models import Signalement
from backend.signalements.serializers import SignalementSerializer
from backend.signalements.view_mixins import (
    SignalementDocumentDownloadViewMixin,
    SignalementViewSetMixin,
)


class SignalementViewSet(SignalementViewSetMixin):
    """
    ViewSet for Signalement model.
    """

    model_class = Signalement
    serializer_class = SignalementSerializer
    model_label = "signalements.Signalement"


@method_decorator(login_required, name="dispatch")
class SignalementDocumentDownloadView(SignalementDocumentDownloadViewMixin):
    """
    Custom view to download the generated document for a signalement.
    """

    model_class = Signalement
