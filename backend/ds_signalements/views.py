from django.utils import dateparse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.ds.champs import DSChamp
from backend.ds.client import DSGraphQLClient
from backend.ds_signalements.ds_mappings import CHAMP_ID_TO_FIELD, DATE_CONSTAT_CHAMP_ID
from backend.ds_signalements.models import DSSignalement
from backend.signalements.serializers import SignalementSerializer
from backend.signalements.view_mixins import (
    SignalementDocumentDownloadViewMixin,
    SignalementViewSetMixin,
)


class ProcessDossierView(APIView):
    def post(self, request):
        dossier_id = request.data.get("dossier_id")
        if not dossier_id or not dossier_id.isdigit():
            return self.bad_request("dossier_id is required and must be an integer")
        numero_dossier = int(dossier_id)
        try:
            ds_client = DSGraphQLClient()
            dossier = ds_client.get_dossier(numero_dossier)
        except Exception as error:
            return self.bad_request(str(error))
        if not dossier:
            return self.bad_request(f"Dossier {dossier_id} not found")
        signalement_data = self.dossier_to_model_data(dossier)
        signalement, _ = DSSignalement.objects.update_or_create(
            ds_numero_dossier=numero_dossier, defaults=signalement_data
        )
        signalement.doc_constat_should_generate = True
        signalement.lettre_info_should_generate = True
        signalement.save()
        signalement_data["id"] = signalement.id
        return Response({**signalement_data, "ds_numero_dossier": numero_dossier})

    def dossier_to_model_data(self, dossier):
        ds_champ = DSChamp(dossier)
        ds_date_depot = self.parse_datetime(dossier.get("dateDepot"))
        ds_date_modification = self.parse_datetime(dossier.get("dateDerniereModification"))
        champs_data = ds_champ.get_data()
        data = {
            "ds_date_depot": ds_date_depot,
            "ds_date_modification": ds_date_modification,
        }
        for champ_id, value in champs_data.items():
            field_name = CHAMP_ID_TO_FIELD.get(champ_id)
            if field_name and value not in (None, "", []):
                data[field_name] = value
        datetime_constat = champs_data[DATE_CONSTAT_CHAMP_ID]
        if datetime_constat:
            data["date_constat"] = datetime_constat.date()
            data["heure_constat"] = datetime_constat.time()
        data["commune"] = data["localisation_depot"].split(" ")[-1]
        return data

    def parse_datetime(self, date_string):
        if not date_string:
            return None
        return dateparse.parse_datetime(date_string)

    def bad_request(self, message):
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


class DSSignalementViewSet(SignalementViewSetMixin):
    """
    ViewSet for DSSignalement model.
    """

    model_class = DSSignalement
    serializer_class = SignalementSerializer
    model_label = "ds_signalements.DSSignalement"
    send_contact_email_enabled = False


class DSSignalementDocumentDownloadView(SignalementDocumentDownloadViewMixin):
    """
    Download documents for DSSignalement instances.
    """

    model_class = DSSignalement
