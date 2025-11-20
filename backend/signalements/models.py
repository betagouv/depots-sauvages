import logging

from django.db import models
from django.template.loader import render_to_string
from model_utils.models import TimeStampedModel

from backend.email_sending.handlers import EmailHandler
from backend.signalements.base import AbstractSignalementBase
from backend.signalements.prejudice import PrejudiceMixin

logger = logging.getLogger(__name__)


class Signalement(AbstractSignalementBase, PrejudiceMixin, TimeStampedModel):
    """
    Model for waste deposit reports
    """

    class Meta:
        verbose_name = "signalement"
        verbose_name_plural = "signalements"

    def __str__(self):
        return f"Dépôt à {self.commune} le {self.date_constat}"

    def send_contact_person_email(self):
        """
        Send email to contact person with signalement documents.
        """
        if not self.contact_email:
            raise ValueError("Contact email is required")
        subject = f"Documents du signalement #{self.id} - {self.commune}"
        html_template = render_to_string("email-get-documents.html", {"signalement": self})
        handler = EmailHandler(
            subject=subject, html_template=html_template, to_emails=[self.contact_email]
        )
        logger.info(f"Sending email for signalement {self.id}")
        if not self.doc_constat:
            logger.warning(
                f"Missing doc_constat for signalement {self.id} - "
                f"email will be sent without rapport de constatation"
            )
        if not self.lettre_info:
            logger.warning(
                f"Missing lettre_info for signalement {self.id} - "
                f"email will be sent without lettre d'information"
            )
        if self.doc_constat:
            handler.add_attachment(
                filename=f"rapport-constatation-{self.id}-{self.commune}.odt",
                content=self.doc_constat,
                mimetype="application/vnd.oasis.opendocument.text",
            )
        if self.lettre_info:
            handler.add_attachment(
                filename=f"lettre-info-{self.id}-{self.commune}.odt",
                content=self.lettre_info,
                mimetype="application/vnd.oasis.opendocument.text",
            )
        return handler.send()
