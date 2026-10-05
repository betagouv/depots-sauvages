import logging

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.proconnect.emails import send_proconnect_access_request_notification_task
from backend.proconnect.models import ProConnectAccessConfig
from backend.proconnect.serializers import (
    ProConnectAccessConfigSerializer,
    ProConnectAccessRequestSerializer,
)

logger = logging.getLogger(__name__)


class ProConnectRejectedInfoView(APIView):
    """
    Returns metadata about the rejected organization stored in session
    during the OIDC authentication step.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        rejected_info = request.session.get("proconnect_rejected_info")
        if not rejected_info:
            return Response(
                {"error": "Aucune information de connexion rejetée trouvée en session."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(rejected_info, status=status.HTTP_200_OK)


class ProConnectAccessRequestView(APIView):
    """
    Allows a user whose ProConnect access was denied to submit an access request.
    Enqueues an asynchronous email notification to admin with details and direct admin link.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        rejected_info = request.session.get("proconnect_rejected_info")
        if not rejected_info or not rejected_info.get("email"):
            return Response(
                {
                    "error": "Aucune session ProConnect active n'a été trouvée pour formuler cette demande."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = ProConnectAccessRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        merged_data = {
            "siret": rejected_info.get("siret", ""),
            "siren": rejected_info.get("siren", ""),
            "organization_label": rejected_info.get("organization_label", ""),
            "email": rejected_info.get("email", ""),
            "name": rejected_info.get("name", ""),
            "message": serializer.validated_data.get("message", ""),
        }
        admin_url_name = getattr(settings, "ADMIN_URL_NAME", "admin").rstrip("/")
        admin_path = f"/{admin_url_name}/proconnect/proconnectaccessconfig/"
        admin_link = request.build_absolute_uri(admin_path) if request else admin_path
        send_proconnect_access_request_notification_task.enqueue(merged_data, admin_link)
        return Response(
            {"success": True, "message": "Votre demande a été transmise à notre équipe."},
            status=status.HTTP_200_OK,
        )


class ProConnectAccessConfigView(APIView):
    """
    API endpoint for viewing and updating ProConnect access restrictions.
    Restricted to staff users.
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        config = ProConnectAccessConfig.get_solo()
        serializer = ProConnectAccessConfigSerializer(config)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        config = ProConnectAccessConfig.get_solo()
        serializer = ProConnectAccessConfigSerializer(config, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        logger.info(
            "ProConnect access config updated by user %s (%s). Sirens count: %d, Categories count: %d",
            request.user.pk,
            request.user.username,
            len(serializer.validated_data.get("sirens_autorises", [])),
            len(serializer.validated_data.get("categories_juridiques_autorisees", [])),
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
