import logging

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


class EmailHandler:
    """
    Utility class to send emails through Django's email backend.
    Handles email creation and sending with attachments.
    """

    def __init__(self, subject, html_template, to_emails):
        """
        Initialize the email sender given the subject, html template and list of
        recipient email addresses.
        """
        self.subject = subject
        self.html_template = html_template
        self.to_emails = to_emails if isinstance(to_emails, list) else [to_emails]
        self.from_email = settings.DEFAULT_FROM_EMAIL
        self.attachments = []

    def add_attachment(self, filename, content, mimetype):
        """
        Add an attachment to the email
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
        logger.info(f"Sending email with {len(self.attachments)} attachments")
        for attachment in self.attachments:
            logger.debug(
                f"Attaching file: {attachment['filename']} "
                f"(size: {len(attachment['content'])} bytes)"
            )
            msg.attach(
                filename=attachment["filename"],
                content=attachment["content"],
                mimetype=attachment["mimetype"],
            )
        try:
            result = msg.send()
            logger.info(f"Email sent successfully with {len(self.attachments)} attachments")
            return result
        except Exception as e:
            logger.error(f"Failed to send email with attachments: {e}")
            raise
