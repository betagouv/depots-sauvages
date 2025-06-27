from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.antispam_timer.timer import FormTimer
from backend.email_sending.handlers import EmailHandler
from backend.email_sending.serializers import EmailSerializer
from backend.signalements.models import Signalement
from backend.throttling.throttles import EmailRateThrottle


class SendEmailViewSet(viewsets.ViewSet):
    """
    ViewSet for handling email sending operations.
    """

    throttle_classes = [EmailRateThrottle]

    @action(detail=True, methods=["post"])
    def send_email(self, request, pk=None):
        """
        Send an email with the signalement documents to the specified email address.
        """
        signalement = get_object_or_404(Signalement, id=pk)
        serializer = EmailSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data["email"]
        subject = f"Documents du signalement #{signalement.id} - {signalement.commune}"
        html_template = render_to_string("email-get-documents.html", {"signalement": signalement})
        handler = EmailHandler(subject=subject, html_template=html_template, to_emails=[email])
        if signalement.doc_constat:
            handler.add_attachment(
                filename=f"rapport-constatation-{signalement.id}-{signalement.commune}.odt",
                content=signalement.doc_constat,
                mimetype="application/vnd.oasis.opendocument.text",
            )
        if signalement.lettre_info:
            handler.add_attachment(
                filename=f"lettre-info-{signalement.id}-{signalement.commune}.odt",
                content=signalement.lettre_info,
                mimetype="application/vnd.oasis.opendocument.text",
            )
        if handler.send():
            # Reset timer after successful email sending
            FormTimer.start_timer(request, settings.TIMER_BASE_NAME)
            return Response({"message": "Email sent successfully"})
        return Response(
            {"error": "Email service unavailable"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
