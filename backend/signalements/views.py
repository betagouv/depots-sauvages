import io

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import View
from rest_framework import viewsets

from backend.signalements.models import Signalement
from backend.signalements.serializers import SignalementSerializer


class SignalementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Signalement model.
    """

    queryset = Signalement.objects.all()
    serializer_class = SignalementSerializer


class SignalementDocumentDownloadView(View):
    """
    Custom view to download the generated document for a signalement.
    """

    def prepare_odt_response(self, signalement):
        if not signalement.doc_constat:
            raise Http404("Rapport de constatation not yet generated")
        return {
            "file": io.BytesIO(signalement.doc_constat),
            "content_type": "application/vnd.oasis.opendocument.text",
            "filename": f"signalement-{signalement.id}-{signalement.commune}.odt",
        }

    def get_doc_constat_response(self, signalement):
        response_data = self.prepare_odt_response(signalement)
        return FileResponse(
            response_data["file"],
            content_type=response_data["content_type"],
            as_attachment=True,
            filename=response_data["filename"],
        )

    def get(self, request, pk):
        """
        Handle GET request to download the document.
        """
        signalement = get_object_or_404(Signalement, pk=pk)
        return self.get_doc_constat_response(signalement)
