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

    def prepare_pdf_response(self, signalement):
        if not signalement.pdf_document:
            raise Http404("PDF document not yet generated")
        return {
            "file": io.BytesIO(signalement.pdf_document),
            "content_type": "application/pdf",
            "filename": f"signalement-{signalement.id}-{signalement.commune}.pdf",
        }

    def prepare_odt_response(self, signalement):
        if not signalement.document:
            raise Http404("ODT document not yet generated")
        return {
            "file": io.BytesIO(signalement.document),
            "content_type": "application/vnd.oasis.opendocument.text",
            "filename": f"signalement-{signalement.id}-{signalement.commune}.odt",
        }

    def get_document_response(self, signalement, format):
        if format == "pdf":
            response_data = self.prepare_pdf_response(signalement)
        else:
            response_data = self.prepare_odt_response(signalement)
        return FileResponse(
            response_data["file"],
            content_type=response_data["content_type"],
            as_attachment=True,
            filename=response_data["filename"],
        )

    def get(self, request, pk, format=None):
        """
        Handle GET request to download the document.
        """
        signalement = get_object_or_404(Signalement, pk=pk)
        return self.get_document_response(signalement, format)
