import logging
import time

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_tasks import task

from backend.doc_maker import odt_utils
from backend.signalements.models import Signalement

logger = logging.getLogger(__name__)


def save_documents(instance, odt_data):
    """
    Save document data to the instance.
    """
    # Prevent infinite loop
    post_save.disconnect(generate_document, sender=Signalement)
    try:
        if odt_data:
            instance.document = odt_data
        instance.document_generated_at = timezone.now()
        instance.save()
        logger.info(f"Document saved for signalement {instance.id}")
    finally:
        post_save.connect(generate_document, sender=Signalement)


@task(queue_name="documents")
def generate_document_task(signalement_id):
    """
    Generate document in background.
    """
    start_time = time.time()
    logger.info(f"Starting document generation for signalement {signalement_id}")
    try:
        instance = Signalement.objects.get(id=signalement_id)
        context = odt_utils.prepare_context(instance)
        logger.debug("Context prepared for document generation")
        output_odt_path = odt_utils.generate_odt_document(instance, context)
        logger.debug("ODT document generated")
        odt_data = odt_utils.read_odt_document(output_odt_path)
        logger.debug("ODT document read")
        save_documents(instance, odt_data)
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Generation completed for signalement {instance.id} in {duration:.2f} seconds")
        return {
            "status": "success",
            "signalement_id": instance.id,
            "duration": duration,
        }
    except Exception as e:
        logger.error(
            f"Error generating document for signalement {signalement_id}: {e}", exc_info=True
        )
        raise  # Let django-tasks handle retries


@receiver(post_save, sender=Signalement)
def generate_document(sender, instance, created, **kwargs):
    """
    Signal handler to trigger document generation when a Signalement is saved.
    Only triggers if generate_doc flag is True.
    """
    if not instance.generate_doc:
        return
    logger.info(f"Post-save signal for signalement {instance.id}, starting background generation")
    generate_document_task.enqueue(instance.id)
    logger.info(f"Document generation task enqueued for signalement {instance.id}")
