from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ProcessDossierView(APIView):
    """
    API endpoint to receive a dossier ID and process it.
    """

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
        return Response({"message": f"Dossier {dossier_id} received", "dossier_id": dossier_id})
