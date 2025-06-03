import logging
import time

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_tasks import task

from backend.doc_maker import odt_utils
from backend.signalements.models import Signalement

logger = logging.getLogger(__name__)


def save_document(instance, odt_data, doc_base_name):
    """
    Save document data to the instance.
    """
    signal_handler = None
    if doc_base_name == "doc_constat":
        signal_handler = generate_doc_constat
    elif doc_base_name == "lettre_info":
        signal_handler = generate_lettre_info
    if not signal_handler:
        return
    post_save.disconnect(signal_handler, sender=Signalement)  # Prevent infinite loop
    try:
        if odt_data:
            setattr(instance, doc_base_name, odt_data)
        setattr(instance, f"{doc_base_name}_generated_at", timezone.now())
        if doc_base_name == "lettre_info":
            setattr(instance, f"{doc_base_name}_should_generate", False)
        instance.save()
        logger.info(f"Document '{doc_base_name}' saved for signalement {instance.id}")
    finally:
        post_save.connect(signal_handler, sender=Signalement)


@task(queue_name="documents")
def generate_document_task(signalement_id, doc_base_name):
    """
    Generate document in background.
    """
    start_time = time.time()
    logger.info(f"Starting {doc_base_name} generation for signalement {signalement_id}")
    try:
        instance = Signalement.objects.get(id=signalement_id)
        context = odt_utils.prepare_context(instance)
        logger.debug(f"Context prepared for {doc_base_name} generation")

        # Generate document based on type
        if doc_base_name == "doc_constat":
            output_odt_path = odt_utils.generate_odt_document(instance, context)
        else:
            output_odt_path = odt_utils.generate_lettre_info(instance, context)

        logger.debug(f"{doc_base_name} generated")
        odt_data = odt_utils.read_odt_document(output_odt_path)
        logger.debug(f"{doc_base_name} read")
        save_document(instance, odt_data, doc_base_name)

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
            f"Error generating {doc_base_name} for signalement {signalement_id}: {e}", exc_info=True
        )
        raise  # Let django-tasks handle retries


@receiver(post_save, sender=Signalement)
def generate_doc_constat(sender, instance, created, **kwargs):
    """
    Signal handler to trigger rapport de constatation generation when a Signalement is saved.
    Only triggers if doc_constat_should_generate flag is True.
    """
    logger.debug(
        f"Signal for {instance.id} with generate doc: " f"{instance.doc_constat_should_generate}"
    )
    if not instance.doc_constat_should_generate:
        return
    logger.info(f"Post-save signal for signalement {instance.id}, starting background generation")
    generate_document_task.enqueue(instance.id, doc_base_name="doc_constat")
    logger.info(f"Document generation task enqueued for signalement {instance.id}")


@receiver(post_save, sender=Signalement)
def generate_lettre_info(sender, instance, created, **kwargs):
    """
    Signal handler to trigger lettre info generation when a Signalement is saved.
    Only triggers if lettre_info_should_generate flag is True.
    """
    logger.debug(
        f"Signal for {instance.id} with generate lettre info: "
        f"{instance.lettre_info_should_generate}"
    )
    if not instance.lettre_info_should_generate:
        return
    logger.info(f"Post-save signal for signalement {instance.id}, starting background generation")
    generate_document_task.enqueue(instance.id, doc_base_name="lettre_info")
    logger.info(f"Lettre info generation task enqueued for signalement {instance.id}")
