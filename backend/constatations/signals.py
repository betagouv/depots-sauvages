import logging
import time

from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_tasks import task

from backend.constatations.models import Constatation
from backend.doc_maker import odt_utils

logger = logging.getLogger(__name__)


def save_document(instance, odt_data, doc_base_name):
    """
    Save document data to the instance.
    """
    sender_model = instance.__class__
    post_save.disconnect(generate_doc_constat, sender=sender_model)
    post_save.disconnect(generate_lettre_info, sender=sender_model)
    try:
        if odt_data:
            setattr(instance, doc_base_name, odt_data)
        setattr(instance, f"{doc_base_name}_generated_at", timezone.now())
        setattr(instance, f"{doc_base_name}_should_generate", False)
        instance.save()
        logger.info(f"Document '{doc_base_name}' saved for constatation {instance.id}")
    finally:
        post_save.connect(generate_doc_constat, sender=sender_model)
        post_save.connect(generate_lettre_info, sender=sender_model)


def generate_document(signalement_id, doc_base_name, model_label):
    """
    Generate document synchronously.
    """
    start_time = time.time()
    logger.info(f"Starting {doc_base_name} generation for constatation {signalement_id}")
    try:
        app_label, model_name = model_label.split(".")
        SignalementModel = apps.get_model(app_label, model_name)
        instance = SignalementModel.objects.get(id=signalement_id)
        context = odt_utils.prepare_context(instance)
        logger.debug(f"Context prepared for {doc_base_name} generation")
        # Generate document based on type
        if doc_base_name == "doc_constat":
            output_odt_path = odt_utils.generate_doc_constat(instance, context)
        else:
            output_odt_path = odt_utils.generate_lettre_info(instance, context)
        logger.debug(f"{doc_base_name} generated")
        odt_data = odt_utils.read_odt_document(output_odt_path)
        logger.debug(f"{doc_base_name} read")
        save_document(instance, odt_data, doc_base_name)
        end_time = time.time()
        duration = end_time - start_time
        logger.info(
            f"Generation completed for constatation {instance.id} in {duration:.2f} seconds"
        )
        return {
            "status": "success",
            "signalement_id": instance.id,
            "duration": duration,
        }
    except Exception as e:
        logger.error(
            f"Error generating {doc_base_name} for constatation {signalement_id}: {e}",
            exc_info=True,
        )
        raise


@task(queue_name="default")
def generate_document_task(signalement_id, doc_base_name, model_label):
    """
    Generate document in background.
    """
    logger.info(
        f"Document generation task started for constatation {signalement_id}, "
        f"document {doc_base_name} ({model_label})"
    )
    try:
        result = generate_document(signalement_id, doc_base_name, model_label)
        logger.info(
            f"Document generation task completed successfully for constatation "
            f"{signalement_id}, document {doc_base_name}"
        )
        return result
    except Exception as e:
        logger.error(
            f"Document generation task failed for constatation {signalement_id}, "
            f"document {doc_base_name}: {e}",
            exc_info=True,
        )
        raise


@receiver(post_save, sender=Constatation)
def generate_doc_constat(sender, instance, created, **kwargs):
    """
    Signal handler to trigger rapport de constatation generation when a Constatation
    is saved. Only triggers if doc_constat_should_generate flag is True.
    """
    logger.debug(
        f"Signal for constatation {instance.id} with generate doc: "
        f"{instance.doc_constat_should_generate}"
    )
    if not instance.doc_constat_should_generate:
        return
    logger.info(f"Post-save signal for constatation {instance.id}, starting background generation")
    model_label = f"{instance._meta.app_label}.{instance._meta.model_name}"
    generate_document_task.enqueue(
        instance.id,
        doc_base_name="doc_constat",
        model_label=model_label,
    )
    logger.info(f"Document generation task enqueued for constatation {instance.id}")


@receiver(post_save, sender=Constatation)
def generate_lettre_info(sender, instance, created, **kwargs):
    """
    Signal handler to trigger lettre info generation when a Constatation
    is saved. Only triggers if lettre_info_should_generate flag is True.
    """
    logger.debug(
        f"Signal for constatation {instance.id} with generate lettre info: "
        f"{instance.lettre_info_should_generate}"
    )
    if not instance.lettre_info_should_generate:
        return
    logger.info(f"Post-save signal for constatation {instance.id}, starting background generation")
    model_label = f"{instance._meta.app_label}.{instance._meta.model_name}"
    generate_document_task.enqueue(
        instance.id,
        doc_base_name="lettre_info",
        model_label=model_label,
    )
    logger.info(f"Lettre info generation task enqueued for constatation {instance.id}")


@receiver(post_save, sender=Constatation)
def create_suivi_procedure(sender, instance, created, **kwargs):
    """
    Ensure that every Constatation has an associated SuiviProcedure as soon as it is saved.
    """
    from backend.procedures.models import SuiviProcedure

    if created:
        SuiviProcedure.objects.get_or_create(constatation=instance)
