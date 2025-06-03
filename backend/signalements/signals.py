import logging
import time

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_tasks import task

from backend.doc_maker import odt_utils
from backend.signalements.models import Signalement

logger = logging.getLogger(__name__)


def save_doc_constat(instance, odt_data):
    """
    Save document data to the instance.
    """
    # Prevent infinite loop
    post_save.disconnect(generate_doc_constat, sender=Signalement)
    try:
        if odt_data:
            instance.doc_constat = odt_data
        instance.doc_constat_generated_at = timezone.now()
        instance.save()
        logger.info(f"Document 'constatation' saved for signalement {instance.id}")
    finally:
        post_save.connect(generate_doc_constat, sender=Signalement)


def save_lettre_info(instance, odt_data):
    """
    Save lettre info data to the instance.
    """
    # Prevent infinite loop
    post_save.disconnect(generate_lettre_info, sender=Signalement)
    try:
        if odt_data:
            instance.lettre_info = odt_data
        instance.lettre_info_generated_at = timezone.now()
        instance.lettre_info_should_generate = False
        instance.save()
        logger.info(f"Lettre info saved for signalement {instance.id}")
    finally:
        post_save.connect(generate_lettre_info, sender=Signalement)


@task(queue_name="documents")
def generate_doc_constat_task(signalement_id):
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
        save_doc_constat(instance, odt_data)
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


@task(queue_name="documents")
def generate_lettre_info_task(signalement_id):
    """
    Generate lettre info in background.
    """
    start_time = time.time()
    logger.info(f"Starting lettre info generation for signalement {signalement_id}")
    try:
        instance = Signalement.objects.get(id=signalement_id)
        context = odt_utils.prepare_context(instance)
        logger.debug("Context prepared for lettre info generation")
        output_odt_path = odt_utils.generate_lettre_info(instance, context)
        logger.debug("Lettre info generated")
        odt_data = odt_utils.read_odt_document(output_odt_path)
        logger.debug("Lettre info read")
        save_lettre_info(instance, odt_data)
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
            f"Error generating lettre info for signalement {signalement_id}: {e}", exc_info=True
        )
        raise  # Let django-tasks handle retries


@receiver(post_save, sender=Signalement)
def generate_doc_constat(sender, instance, created, **kwargs):
    """
    Signal handler to trigger rapport de constatation generation when a Signalement is saved.
    Only triggers if doc_constat_should_generate flag is True.
    """
    logger.debug(
        f"Signal for {instance.id} with generate doc: {instance.doc_constat_should_generate}"
    )
    if not instance.doc_constat_should_generate:
        return
    logger.info(f"Post-save signal for signalement {instance.id}, starting background generation")
    generate_doc_constat_task.enqueue(instance.id)
    logger.info(f"Document generation task enqueued for signalement {instance.id}")


@receiver(post_save, sender=Signalement)
def generate_lettre_info(sender, instance, created, **kwargs):
    """
    Signal handler to trigger lettre info generation when a Signalement is saved.
    Only triggers if lettre_info_should_generate flag is True.
    """
    logger.debug(
        f"Signal for {instance.id} with generate lettre info: {instance.lettre_info_should_generate}"
    )
    if not instance.lettre_info_should_generate:
        return
    logger.info(f"Post-save signal for signalement {instance.id}, starting background generation")
    generate_lettre_info_task.enqueue(instance.id)
    logger.info(f"Lettre info generation task enqueued for signalement {instance.id}")
