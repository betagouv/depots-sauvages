import logging

from django.contrib.auth.decorators import login_required
from django.utils import dateparse
from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.dn.fields import DNField
from backend.dn.client import DNGraphQLClient
from backend.dn_signalements.dn_mappings import (
    CHAMP_ID_ADRESSE_AUTEUR,
    CHAMP_ID_ADRESSE_DEPOT,
    CHAMP_ID_SIRET,
    CHAMP_ID_TO_FIELD,
    DATE_CONSTAT_CHAMP_ID,
)
from backend.dn_signalements.models import DNSignalement, UserDossier
from backend.dn_signalements.serializers import UserDossierSerializer
from backend.dn_signalements.tasks import sync_user_dossiers
from backend.signalements.views import SignalementDocumentDownloadViewMixin


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
            logging.exception(f"Error fetching dossier with id %s. \n {e}", dossier_id)
            return self.bad_request("Une erreur est survenue lors de la récupération du dossier")
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
        # Map metadata back to model fields since model is not changing yet
        model_defaults = {
            **signalement_data,
            "dn_date_creation": dn_metadata.get("dn_date_creation"),
            "dn_date_modification": dn_metadata.get("dn_date_modification"),
        }
        signalement, _ = DNSignalement.objects.update_or_create(
            dn_numero_dossier=numero_dossier, defaults=model_defaults
        )
        signalement.doc_constat_should_generate = True
        signalement.lettre_info_should_generate = True
        signalement.save()
        signalement_data["id"] = signalement.id
        return Response(
            {
                **signalement_data,
                "dn_numero_dossier": numero_dossier,
                "created": True,
                **dn_metadata,
            }
        )

    def extract_dn_metadata(self, dossier):
        """Extract DN administrative metadata."""
        date_creation = self.parse_datetime(dossier.get("dateDepot"))
        date_modification = self.parse_datetime(dossier.get("dateDerniereModification"))
        return {
            "date_creation": date_creation,
            "date_modification": date_modification,
            "dn_date_creation": date_creation,
            "dn_date_modification": date_modification,
        }

    def dossier_to_model_data(self, dossier):
        """Extract signalement data from DN dossier. Returns None if no signalement exists."""
        dn_field = DNField(dossier)
        fields_data = dn_field.get_data()
        datetime_constat = fields_data.get(DATE_CONSTAT_CHAMP_ID)
        if not datetime_constat:
            return None
        data = {
            "date_constat": datetime_constat,
            "heure_constat": datetime_constat.time(),
        }
        for champ_id, value in fields_data.items():
            field_name = CHAMP_ID_TO_FIELD.get(champ_id)
            if field_name and value not in (None, "", []):
                data[field_name] = value
        data.update(self.get_siret_auto_completion_data(fields_data, data))
        data.update(self.get_address_data(fields_data))
        data.update(self.get_normalized_data(data))
        data.update(self.get_usager_contact_data(dossier))
        return data

    def get_siret_auto_completion_data(self, fields_data, data):
        updates = {}
        siret_data = fields_data.get(CHAMP_ID_SIRET)
        if siret_data and isinstance(siret_data, dict):
            updates["auteur_siret"] = siret_data.get("siret", "")
            name = siret_data.get("nom")
            address_dict = siret_data.get("adresse_dict")
            if name and not data.get("auteur_nom"):
                updates["auteur_nom"] = name
            if address_dict and not data.get("auteur_adresse"):
                updates["auteur_adresse"] = self.format_address(address_dict)
        return updates

    def get_address_data(self, fields_data):
        updates = {}
        depot_address_data = fields_data.get(CHAMP_ID_ADRESSE_DEPOT)
        if depot_address_data and isinstance(depot_address_data, dict):
            label = depot_address_data.get("label", "")
            updates["localisation_depot"] = self.clean_text(label, join_with=" ")
            if depot_address_data.get("cityName"):
                updates["commune"] = depot_address_data["cityName"]
        author_address_data = fields_data.get(CHAMP_ID_ADRESSE_AUTEUR)
        if author_address_data and isinstance(author_address_data, dict):
            updates["auteur_adresse"] = self.format_address(author_address_data)
        return updates

    def format_address(self, address_dict):
        if not address_dict or not isinstance(address_dict, dict):
            return ""
        street = address_dict.get("streetAddress")
        zip_code = address_dict.get("postalCode")
        city = address_dict.get("cityName")
        if street and zip_code:
            return self.clean_text(f"{street}\n{zip_code} {city or ''}")
        return self.clean_text(address_dict.get("label", ""))

    def clean_text(self, text, join_with="\n"):
        if not text:
            return ""
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        return join_with.join([line.strip() for line in text.splitlines() if line.strip()])

    def get_normalized_data(self, data):
        updates = {}
        if data.get("statut_auteur"):
            statut_lower = str(data["statut_auteur"]).lower()
            if "entreprise" in statut_lower:
                updates["statut_auteur"] = "entreprise"
            elif "particulier" in statut_lower:
                updates["statut_auteur"] = "particulier"
        if data.get("nature_terrain") and isinstance(data["nature_terrain"], list):
            updates["nature_terrain"] = [str(item).lower() for item in data["nature_terrain"]]
        if data.get("auteur_adresse"):
            updates["auteur_adresse"] = self.clean_text(data["auteur_adresse"])
        return updates

    def get_usager_contact_data(self, dossier):
        updates = {}
        usager = dossier.get("usager", {})
        if usager.get("email"):
            updates["contact_email"] = usager["email"]
        demandeur = dossier.get("demandeur", {})
        if demandeur.get("nom"):
            updates["contact_nom"] = demandeur["nom"]
        if demandeur.get("prenom"):
            updates["contact_prenom"] = demandeur["prenom"]
        return updates

    def parse_datetime(self, date_string):
        if not date_string:
            return None
        return dateparse.parse_datetime(date_string)

    def bad_request(self, message):
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(login_required, name="dispatch")
class DNSignalementDocumentDownloadView(SignalementDocumentDownloadViewMixin):
    """
    Download documents for DNSignalement instances.
    """

    model_class = DNSignalement


class UserDossierViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List user dossiers with statuses, from the database.
    """

    serializer_class = UserDossierSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserDossier.objects.filter(user=self.request.user).order_by("-date_creation")


class SyncUserDossiersView(APIView):
    """
    Trigger a background synchronization of user dossiers.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        sync_user_dossiers.enqueue(request.user.id)
        return Response({"status": "sync_triggered"}, status=status.HTTP_202_ACCEPTED)
