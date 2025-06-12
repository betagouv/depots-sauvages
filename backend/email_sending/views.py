from django.template.loader import render_to_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.email_sending.handlers import EmailHandler
from backend.email_sending.serializers import EmailSerializer
from backend.signalements.models import Signalement


class SendEmailViewSet(viewsets.ViewSet):
    """
    ViewSet for handling email sending operations.
    """

    @action(detail=True, methods=["post"])
    def send_signalement(self, request, pk=None):
        """
        Send an email with the signalement documents to the specified email address.
        """
        try:
            signalement = Signalement.objects.get(id=pk)
            serializer = EmailSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            email = serializer.validated_data["email"]
            subject = f"Documents du signalement #{signalement.id} - {signalement.commune}"
            html_template = render_to_string(
                "email-get-documents.html", {"signalement": signalement}
            )
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
                return Response({"message": "Email sent successfully"})
            else:
                return Response(
                    {"error": "Failed to send email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Signalement.DoesNotExist:
            return Response({"error": "Signalement not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
