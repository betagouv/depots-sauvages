import io

from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View
from rest_framework import mixins, permissions, viewsets
from rest_framework.response import Response

from backend.activity_logs.views import TrackActivityMixin
from backend.constatations.concurrency import check_optimistic_lock
from backend.teams.models import get_user_team, get_user_team_id

from .models import Constatation
from .serializers import ConstatationListSerializer, ConstatationSerializer


def get_user_constatations_queryset(user):
    """
    Returns the queryset of Constatation instances accessible by the user.
    - Staff members: access to all constatations.
    - User with team: access to all constatations belonging to the same team.
    - User without team: access strictly to constatations with team__isnull=True
      and created_by=user (fallback to user=user if created_by is null).
    """
    if not user or not user.is_authenticated or not getattr(user, "is_active", True):
        return Constatation.objects.none()
    if user.is_staff:
        return Constatation.objects.all()
    user_team_id = get_user_team_id(user)
    if user_team_id:
        return Constatation.objects.filter(team_id=user_team_id)
    return Constatation.objects.filter(
        models.Q(team__isnull=True)
        & (models.Q(created_by=user) | models.Q(created_by__isnull=True, user=user))
    )


class ConstatationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
    TrackActivityMixin,
):
    serializer_class = ConstatationSerializer
    permission_classes = [permissions.IsAuthenticated]

    DOCUMENT_BINARY_FIELDS = ("doc_constat", "lettre_info")

    def get_serializer_class(self):
        if self.action == "list":
            return ConstatationListSerializer
        return ConstatationSerializer

    def get_queryset(self):
        qs = (
            get_user_constatations_queryset(self.request.user)
            .defer(*self.DOCUMENT_BINARY_FIELDS)
            .order_by("-modified")
        )
        if self.action == "list":
            return qs.defer("photos").select_related("suivi_procedure")
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        team = get_user_team(user)
        instance = serializer.save(
            user=user,
            team=team,
            created_by=user,
            updated_by=user,
        )
        self._track(
            action="constatation_demarree",
            target="constatation",
            constatation_id=instance.id,
            commune=instance.commune,
            constatant_role=instance.constatant_role,
        )

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
        was_draft = serializer.instance.is_draft
        user = self.request.user
        update_kwargs = {"updated_by": user}
        if serializer.instance.created_by is None:
            update_kwargs["created_by"] = serializer.instance.user or user
        instance = serializer.save(**update_kwargs)
        if was_draft and not instance.is_draft:
            action = "constatation_terminee"
        elif instance.is_draft:
            action = "constatation_demarree"
        else:
            return
        extra_data = {}
        if action == "constatation_terminee":
            extra_data["auteur_identifie"] = instance.auteur_identifie
        self._track(
            action=action,
            target="constatation",
            constatation_id=instance.id,
            commune=instance.commune,
            constatant_role=instance.constatant_role,
            **extra_data,
        )


@method_decorator(login_required, name="dispatch")
class ConstatationDocumentDownloadView(View, TrackActivityMixin):
    """
    Download documents for Constatation instances securely.
    """

    model_class = Constatation

    def _get_constatation(self, pk):
        return get_object_or_404(get_user_constatations_queryset(self.request.user), pk=pk)

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
        action = (
            "doc_constat_telecharge" if doc_type == "doc-constat" else "lettre_info_telechargee"
        )
        self._track(
            action=action,
            target="document",
            constatation_id=constatation.id,
            type_document=doc_type,
        )
        return FileResponse(
            response_data["file"],
            content_type=response_data["content_type"],
            as_attachment=True,
            filename=response_data["filename"],
        )
