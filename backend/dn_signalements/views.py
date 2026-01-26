import logging

from django.contrib.auth.decorators import login_required
from django.utils import dateparse
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.dn.champs import DNChamp
from backend.dn.client import DNGraphQLClient
from backend.dn_signalements.dn_mappings import (
    ADDRESS_CHAMP_ID,
    CHAMP_ID_TO_FIELD,
    DATE_CONSTAT_CHAMP_ID,
)
from backend.dn_signalements.models import DNSignalement
from backend.signalements.serializers import SignalementSerializer
from backend.signalements.view_mixins import (
    SignalementDocumentDownloadViewMixin,
    SignalementViewSetMixin,
)


class ProcessDossierView(APIView):
    def post(self, request):
        dossier_id = request.data.get("dossier_id")
        if not dossier_id or not str(dossier_id).isdigit():
            return self.bad_request("dossier_id is required and must be an integer")
        numero_dossier = int(dossier_id)
        try:
            dn_client = DNGraphQLClient()
            dossier = dn_client.get_dossier(numero_dossier)
        except Exception as e:
            logging.exception("Error fetching dossier with id %s", dossier_id)
            return self.bad_request(
                f"Il y a eu une erreur lors de la récupération du dossier." f" {e}"
            )
        if not dossier:
            return self.bad_request(f"Dossier {dossier_id} not found")
        dn_metadata = self.extract_dn_metadata(dossier)
        signalement_data = self.dossier_to_model_data(dossier)
        if signalement_data is None:
            return Response(
                {
                    "created": False,
                    "dn_numero_dossier": numero_dossier,
                    "reason": "no_procedure_or_missing_info",
                    **dn_metadata,
                }
            )
        signalement_data.update(dn_metadata)
        signalement, _ = DNSignalement.objects.update_or_create(
            dn_numero_dossier=numero_dossier, defaults=signalement_data
        )
        signalement.doc_constat_should_generate = True
        signalement.lettre_info_should_generate = True
        signalement.save()
        signalement_data["id"] = signalement.id
        return Response({**signalement_data, "dn_numero_dossier": numero_dossier, "created": True})

    def extract_dn_metadata(self, dossier):
        """Extract DN administrative metadata."""
        return {
            "dn_date_creation": self.parse_datetime(dossier.get("dateDepot")),
            "dn_date_modification": self.parse_datetime(dossier.get("dateDerniereModification")),
        }

    def dossier_to_model_data(self, dossier):
        """Extract signalement data from DN dossier. Returns None if no signalement exists."""
        dn_champ = DNChamp(dossier)
        champs_data = dn_champ.get_data()
        # If there is no date_constat, there is no actual "signalement"
        datetime_constat = champs_data.get(DATE_CONSTAT_CHAMP_ID)
        if not datetime_constat:
            return None
        data = {
            "date_constat": datetime_constat.date(),
            "heure_constat": datetime_constat.time(),
        }
        for champ_id, value in champs_data.items():
            field_name = CHAMP_ID_TO_FIELD.get(champ_id)
            if field_name and value not in (None, "", []):
                data[field_name] = value
        address_data = champs_data.get(ADDRESS_CHAMP_ID)
        if address_data and isinstance(address_data, dict):
            if address_data.get("label"):
                data["localisation_depot"] = address_data["label"]
            if address_data.get("cityName"):
                data["commune"] = address_data["cityName"]
        if data.get("statut_auteur"):
            statut_lower = str(data["statut_auteur"]).lower()
            if "entreprise" in statut_lower:
                data["statut_auteur"] = "entreprise"
            elif "particulier" in statut_lower:
                data["statut_auteur"] = "particulier"
        if data.get("nature_terrain") and isinstance(data["nature_terrain"], list):
            data["nature_terrain"] = [str(item).lower() for item in data["nature_terrain"]]
        usager = dossier.get("usager", {})
        if usager.get("email"):
            data["contact_email"] = usager["email"]
        demandeur = dossier.get("demandeur", {})
        if demandeur.get("nom"):
            data["contact_nom"] = demandeur["nom"]
        if demandeur.get("prenom"):
            data["contact_prenom"] = demandeur["prenom"]
        return data

    def parse_datetime(self, date_string):
        if not date_string:
            return None
        return dateparse.parse_datetime(date_string)

    def bad_request(self, message):
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


class DNSignalementViewSet(SignalementViewSetMixin):
    """
    ViewSet for DNSignalement model.
    """

    model_class = DNSignalement
    serializer_class = SignalementSerializer
    model_label = "dn_signalements.DNSignalement"
    send_contact_email_enabled = False


@method_decorator(login_required, name="dispatch")
class DNSignalementDocumentDownloadView(SignalementDocumentDownloadViewMixin):
    """
    Download documents for DNSignalement instances.
    """

    model_class = DNSignalement
