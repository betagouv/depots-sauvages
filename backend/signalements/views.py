import io

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import View
from rest_framework import viewsets

from backend.signalements.models import Signalement
from backend.signalements.serializers import SignalementSerializer
from backend.throttling.throttles import SignalementRateThrottle


class SignalementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Signalement model.
    """

    queryset = Signalement.objects.all()
    serializer_class = SignalementSerializer
    throttle_classes = [SignalementRateThrottle]


class SignalementDocumentDownloadView(View):
    """
    Custom view to download the generated document for a signalement.
    """

    def prepare_doc_constat(self, signalement):
        if not signalement.doc_constat:
            raise Http404("Rapport de constatation not yet generated")
        return {
            "file": io.BytesIO(signalement.doc_constat),
            "content_type": "application/vnd.oasis.opendocument.text",
            "filename": f"rapport-constatation-{signalement.id}-{signalement.commune}.odt",
        }

    def prepare_lettre_info(self, signalement):
        if not signalement.lettre_info:
            raise Http404("Lettre d'information not yet generated")
        return {
            "file": io.BytesIO(signalement.lettre_info),
            "content_type": "application/vnd.oasis.opendocument.text",
            "filename": f"lettre-info-{signalement.id}-{signalement.commune}.odt",
        }

    def get(self, request, pk, doc_type=None):
        """
        Handle GET request to download the document.
        """
        signalement = get_object_or_404(Signalement, pk=pk)
        if doc_type == "doc-constat":
            response_data = self.prepare_doc_constat(signalement)
        elif doc_type == "lettre-info":
            response_data = self.prepare_lettre_info(signalement)
        else:
            raise Http404("Invalid document type")
        return FileResponse(
            response_data["file"],
            content_type=response_data["content_type"],
            as_attachment=True,
            filename=response_data["filename"],
        )
