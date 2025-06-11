from django.conf import settings
from django.core.mail import EmailMessage


class EmailSender:
    """
    Utility class to send emails through Django's email backend.
    Handles email creation and sending with attachments.
    The actual email provider (SMTP, Brevo, etc.) is configured in Django settings.
    """

    def __init__(self, subject, html_template, to_emails):
        """
        Initialize the email sender.

        Args:
            subject: Email subject
            html_template: HTML content of the email
            to_emails: List of recipient email addresses
        """
        self.subject = subject
        self.html_template = html_template
        self.to_emails = to_emails
        self.from_email = settings.DEFAULT_FROM_EMAIL
        self.attachments = []

    def add_attachment(self, filename, content, mimetype):
        """
        Add an attachment to the email.

        Args:
            filename: Name of the file
            content: Binary content of the file
            mimetype: MIME type of the file
        """
        self.attachments.append({"filename": filename, "content": content, "mimetype": mimetype})

    def send(self):
        """
        Create and send the email with all attachments.
        """
        msg = EmailMessage(
            subject=self.subject,
            body=self.html_template,
            from_email=self.from_email,
            to=self.to_emails,
        )
        msg.content_subtype = "html"
        for attachment in self.attachments:
            msg.attach(
                filename=attachment["filename"],
                content=attachment["content"],
                mimetype=attachment["mimetype"],
            )
        msg.send()


def send_test_email():
    """
    Example function to test the EmailSender with document attachments.
    Gets the first available Signalement with both doc_constat and lettre_info files
    and sends them as attachments.
    """
    from backend.signalements.models import Signalement

    ODT_MIMETYPE = "application/vnd.oasis.opendocument.text"
    # Get the first Signalement with both documents
    signalement = Signalement.objects.filter(
        doc_constat__isnull=False, lettre_info__isnull=False
    ).first()

    if not signalement:
        return

    subject = "Test d'envoi de documents"
    html_template = """
    <html>
        <body>
            <h1>Test d'envoi de documents</h1>
            <p>Ceci est un email de test envoyé via Brevo.</p>
            <p>Les documents suivants sont joints :</p>
            <ul>
                <li>Rapport de constatation</li>
                <li>Lettre d'information</li>
            </ul>
        </body>
    </html>
    """

    sender = EmailSender(
        subject=subject,
        html_template=html_template,
        to_emails=["sylvain.toe@beta.gouv.fr"],
    )

    sender.add_attachment(
        filename=f"rapport-constatation-{signalement.id}-{signalement.commune}.odt",
        content=signalement.doc_constat,
        mimetype=ODT_MIMETYPE,
    )

    sender.add_attachment(
        filename=f"lettre-info-{signalement.id}-{signalement.commune}.odt",
        content=signalement.lettre_info,
        mimetype=ODT_MIMETYPE,
    )

    sender.send()
