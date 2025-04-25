import logging
from pathlib import Path

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.utils import timezone
from python_odt_template.libreoffice import convert_to_pdf

from backend.doc_maker.odt import ODTProcessor
from backend.signalements.models import Signalement

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Signalement)
def generate_document(sender, instance, created, **kwargs):
    """
    Generate document when generate_doc flag is True
    """
    if instance.generate_doc:
        try:
            # Get all model fields as a dictionary
            context = model_to_dict(instance)
            # Remove fields we don't need
            context.pop("id", None)
            context.pop("generate_doc", None)
            context.pop("document", None)
            context.pop("document_generated_at", None)
            context["prejudice_montant_calcule"] = instance.get_prejudice_montant_calcule()
            # Format date and time fields
            if context["date_constat"]:
                context["date_constat"] = context["date_constat"].strftime("%d/%m/%Y")
            if context["heure_constat"]:
                context["heure_constat"] = context["heure_constat"].strftime("%H:%M")
            logger.info(f"Generating document for signalement {instance.id}")
            logger.debug(f"Template context: {context}")
            # Generate ODT document
            processor = ODTProcessor()
            output_odt_path = processor.process_template(
                "template.odt",
                context,
                f"signalement_{instance.id}.odt",
            )
            # Convert to PDF using the library's function
            output_dir = Path(output_odt_path).parent
            convert_to_pdf(output_odt_path, output_dir)
            output_pdf_path = output_dir / f"signalement_{instance.id}.pdf"
            # Store ODT in DB
            with open(output_odt_path, "rb") as f:
                document_data = f.read()
            # Store PDF in DB
            with open(output_pdf_path, "rb") as f:
                pdf_data = f.read()
            # Prevent infinite loop
            post_save.disconnect(generate_document, sender=Signalement)
            try:
                instance.document = document_data
                instance.pdf_document = pdf_data
                instance.document_generated_at = timezone.now()
                instance.save()
                logger.info(f"Documents saved for signalement {instance.id}")
            finally:
                post_save.connect(generate_document, sender=Signalement)
        except Exception as e:
            logger.error(f"Error generating document: {e}", exc_info=True)
