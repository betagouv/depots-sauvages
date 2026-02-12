import io

from django.core.exceptions import ImproperlyConfigured
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import View
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.signalements.signals import send_contact_email_task
from backend.throttling.throttles import SignalementRateThrottle


class SignalementViewSetMixin(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    This mixin contains the core logic for handling signalements
    """

    model_class = None
    serializer_class = None
    model_label = None
    send_contact_email_enabled = True
    throttle_classes = [SignalementRateThrottle]

    def get_queryset(self):
        if not self.model_class:
            raise ImproperlyConfigured("model_class must be set")
        return self.model_class.objects.all()

    @action(detail=True, methods=["post"])
    def send_contact_email(self, request, pk=None):
        """
        Queue email sending for a signalement.
        """
        if not self.send_contact_email_enabled:
            return Response(status=status.HTTP_404_NOT_FOUND)
        signalement = self.get_object()
        if not signalement.contact_email:
            return Response(
                {"error": "No contact email available for this signalement"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        send_contact_email_task.enqueue(signalement.id, model_label=self.model_label)
        return Response({"message": "Contact email queued for sending"})


class SignalementDocumentDownloadViewMixin(View):
    """
    This mixin contains the core logic for handling document downloads
    for a signalement-liked models.
    """

    model_class = None

    def _get_signalement(self, pk):
        if not self.model_class:
            raise Http404("No signalement model configured")
        return get_object_or_404(self.model_class, pk=pk)

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
        signalement = self._get_signalement(pk)
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
