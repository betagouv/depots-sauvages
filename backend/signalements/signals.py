import logging
import threading
import time

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


def generate_document_background(instance):
    """
    Generate document in background thread
    """
    start_time = time.time()
    logger.info(f"Starting document generation for signalement {instance.id}")
    try:
        context = odt_utils.prepare_context(instance)
        logger.debug("Context prepared for document generation")
        output_odt_path = odt_utils.generate_odt_document(instance, context)
        logger.debug("ODT document generated")
        odt_data = odt_utils.read_odt_document(output_odt_path)
        logger.debug("ODT document read")
        pdf_data = pdf_utils.convert_odt_to_pdf(output_odt_path, f"signalement_{instance.id}.pdf")
        logger.debug("PDF document generated")
        save_documents(instance, odt_data, pdf_data)
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Generation completed for signalement {instance.id} in {duration:.2f} seconds")
    except Exception as e:
        logger.error(f"Error generating document for signalement {instance.id}: {e}", exc_info=True)


@receiver(post_save, sender=Signalement)
def generate_document(sender, instance, created, **kwargs):
    """
    Generate document when generate_doc flag is True
    """
    if not instance.generate_doc:
        return
    logger.info(f"Post-save signal for signalement {instance.id}, starting background generation")
    threading.Thread(target=generate_document_background, args=(instance,)).start()
