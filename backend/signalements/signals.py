import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from backend.doc_maker import odt_utils, pdf_utils
from backend.signalements.models import Signalement

logger = logging.getLogger(__name__)


def save_documents(instance, odt_data, pdf_data):
    """
    Save document data to the instance.
    """
    # Prevent infinite loop
    post_save.disconnect(generate_document, sender=Signalement)
    try:
        if odt_data:
            instance.document = odt_data
        if pdf_data:
            instance.pdf_document = pdf_data
        instance.document_generated_at = timezone.now()
        instance.save()
        logger.info(f"Documents saved for signalement {instance.id}")
    finally:
        post_save.connect(generate_document, sender=Signalement)


@receiver(post_save, sender=Signalement)
def generate_document(sender, instance, created, **kwargs):
    """
    Generate document when generate_doc flag is True
    """
    if not instance.generate_doc:
        return
    try:
        context = odt_utils.prepare_context(instance)
        output_odt_path = odt_utils.generate_odt_document(instance, context)
        odt_data = odt_utils.read_odt_document(output_odt_path)
        pdf_data = pdf_utils.convert_odt_to_pdf(output_odt_path, f"signalement_{instance.id}.pdf")
        save_documents(instance, odt_data, pdf_data)
    except Exception as e:
        logger.error(f"Error generating document: {e}", exc_info=True)
