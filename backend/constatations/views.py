import io

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View
from rest_framework import mixins, permissions, viewsets

from .models import Constatation
from .serializers import ConstatationSerializer


class ConstatationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ConstatationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Constatation.objects.filter(user=self.request.user).order_by("-modified")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@method_decorator(login_required, name="dispatch")
class ConstatationDocumentDownloadView(View):
    """
    Download documents for Constatation instances securely.
    """

    model_class = Constatation

    def _get_constatation(self, pk):
        return get_object_or_404(self.model_class, pk=pk, user=self.request.user)

    def prepare_doc_constat(self, constatation):
        if not constatation.doc_constat:
            raise Http404("Rapport de constatation not yet generated")
        return {
            "file": io.BytesIO(constatation.doc_constat),
            "content_type": "application/vnd.oasis.opendocument.text",
            "filename": f"rapport-constatation-{constatation.id}-{constatation.commune}.odt",
        }

    def prepare_lettre_info(self, constatation):
        if not constatation.lettre_info:
            raise Http404("Lettre d'information not yet generated")
        return {
            "file": io.BytesIO(constatation.lettre_info),
            "content_type": "application/vnd.oasis.opendocument.text",
            "filename": f"lettre-info-{constatation.id}-{constatation.commune}.odt",
        }

    def get(self, request, pk, doc_type=None):
        constatation = self._get_constatation(pk)
        if doc_type == "doc-constat":
            response_data = self.prepare_doc_constat(constatation)
        elif doc_type == "lettre-info":
            response_data = self.prepare_lettre_info(constatation)
        else:
            raise Http404("Invalid document type")
        return FileResponse(
            response_data["file"],
            content_type=response_data["content_type"],
            as_attachment=True,
            filename=response_data["filename"],
        )
