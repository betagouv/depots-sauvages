from rest_framework import exceptions, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from trackman.api import TrackingAPIViewMixin

from backend.activity_logs.tracking import IdempotentTrackingHandler
from backend.constatations.models import Constatation
from backend.procedures.models import SuiviProcedure
from backend.stats.anonymizer import anonymize_user_hash

CONSTATATION_ACTIONS = {
    "constatation_demarree",
    "constatation_terminee",
    "doc_constat_telecharge",
    "lettre_info_telechargee",
    "documents_signes_confirme",
    "notification_auteur_envoyee",
    "accuse_reception_enregistre",
    "decision_enregistree",
    "procedure_abandonnee",
    "sanction_decidee",
    "documents_sanction_telecharges",
    "procedure_cloturee",
    "montant_recouvre_enregistre",
}

ACTION_TARGET_MAP = {
    "utilisateur_connecte": "auth",
    "constatation_demarree": "constatation",
    "constatation_terminee": "constatation",
    "doc_constat_telecharge": "document",
    "lettre_info_telechargee": "document",
    "documents_signes_confirme": "suivi_procedure",
    "notification_auteur_envoyee": "suivi_procedure",
    "accuse_reception_enregistre": "suivi_procedure",
    "decision_enregistree": "suivi_procedure",
    "procedure_abandonnee": "suivi_procedure",
    "sanction_decidee": "suivi_procedure",
    "documents_sanction_telecharges": "document",
    "procedure_cloturee": "suivi_procedure",
    "montant_recouvre_enregistre": "suivi_procedure",
    "contact_clic_inscription": "contact",
}


class UserActionTrackingView(TrackingAPIViewMixin, APIView):
    model_alias = "activity_log"
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        action_details = self.clean_action_details(request.data)
        IdempotentTrackingHandler().track_action(action_details, model_alias=self.model_alias)
        return Response(status=status.HTTP_201_CREATED)

    def _resolve_constatation_and_suivi_procedure_ids(self, object_id, action):
        constatation_id = object_id  # The object we looking for is a constatation.
        if not constatation_id or action not in CONSTATATION_ACTIONS:
            return None, None
        try:
            constatation_id = int(object_id)
            if not Constatation.objects.filter(id=constatation_id).exists():
                return None, None
        except (ValueError, TypeError):
            return None, None
        suivi_procedure = SuiviProcedure.objects.filter(constatation_id=constatation_id).first()
        suivi_procedure_id = suivi_procedure.id if suivi_procedure else None
        return constatation_id, suivi_procedure_id

    def clean_action_details(self, action_details):
        details = action_details.copy()
        user = self.request.user
        action = details.get("action")
        if not action:
            raise exceptions.ValidationError({"action": ["Ce champ est obligatoire."]})
        details["actor"] = anonymize_user_hash(user.id)
        details["target"] = details.get("target") or ACTION_TARGET_MAP.get(action, "app")
        object_id = details.get("object")
        constatation_id, suivi_procedure_id = self._resolve_constatation_and_suivi_procedure_ids(
            object_id, action
        )
        if constatation_id:
            details["constatation_id"] = constatation_id
        if suivi_procedure_id:
            details["suivi_procedure_id"] = suivi_procedure_id
        data = details.get("data") or {}
        if not isinstance(data, dict):
            data = {}
        data["user_is_staff"] = user.is_staff
        details["data"] = data
        session_key = getattr(self.request.session, "session_key", None)
        if session_key:
            details["session_id"] = str(session_key)
        return details
