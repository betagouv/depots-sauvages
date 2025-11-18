from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.ds.client import DSGraphQLClient


class ProcessDossierView(APIView):
    """
    API endpoint to receive a dossier ID and process it.
    """

    SENSITIVE_FIELD_IDS = [
        "Q2hhbXAtNTYxNzQ4NA==",  # Numéro de téléphone
        "Q2hhbXAtNTYxNzQ5MQ==",  # NOM de l'auteur présumé responsable
        "Q2hhbXAtNTYxNzQ5Mg==",  # Prénom de l'auteur présumé responsable
        "Q2hhbXAtNTYxNzM2Ng==",  # Localisation du dépôt
        "Q2hhbXAtNDYyODE3Mg==",  # Vous pouvez préciser la géolocalisation
    ]

    def post(self, request):
        """
        Handle POST request to process a dossier.
        """
        dossier_id = request.data.get("dossier_id")
        if not dossier_id:
            return Response(
                {"error": "dossier_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            client = DSGraphQLClient()
            dossier_number = int(dossier_id)
            dossier = client.get_dossier(dossier_number)
            if not dossier:
                return Response(
                    {"error": f"Dossier {dossier_id} not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            response_data = dossier.copy()
            response_data["champs"] = [
                champ
                for champ in dossier.get("champs", [])
                if champ.get("id") not in self.SENSITIVE_FIELD_IDS
            ]
            usager = dossier.get("usager", {})
            if usager:
                response_data["usager"] = {**usager, "email": None}
            return Response(response_data)
        except ValueError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as error:
            return Response(
                {"error": f"Failed to fetch dossier: {str(error)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
