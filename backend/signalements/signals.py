import logging
import tempfile
from pathlib import Path

import convertapi
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.utils import timezone

from backend.doc_maker.odt import ODTProcessor
from backend.doc_maker.settings import OUTPUT_DIR, TEMPLATE_DIR
from backend.signalements.models import Signalement

logger = logging.getLogger(__name__)

# Configure ConvertAPI
if not settings.CONVERTAPI_SECRET:
    logger.warning("ConvertAPI secret is not set. PDF conversion will be disabled.")
else:
    convertapi.api_credentials = settings.CONVERTAPI_SECRET


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
            processor = ODTProcessor()  # This will ensure directories exist
            output_odt_path = processor.process_template(
                str(TEMPLATE_DIR / "template.odt"),
                context,
                str(OUTPUT_DIR / f"signalement_{instance.id}.odt"),
            )
            # Convert ODT to PDF using ConvertAPI
            if settings.CONVERTAPI_SECRET:
                try:
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_pdf_path = Path(temp_dir) / f"signalement_{instance.id}.pdf"
                        convertapi.convert(
                            "pdf", {"File": str(output_odt_path)}, from_format="odt"
                        ).save_files(str(temp_pdf_path))

                        # Read the generated PDF
                        with open(temp_pdf_path, "rb") as f:
                            pdf_data = f.read()
                except Exception as e:
                    logger.error(f"Error converting ODT to PDF: {e}", exc_info=True)
                    pdf_data = None
                # Store ODT in DB
                with open(output_odt_path, "rb") as f:
                    document_data = f.read()
            else:
                logger.warning("Skipping PDF conversion: ConvertAPI not configured properly")
                document_data = None
            # Prevent infinite loop
            post_save.disconnect(generate_document, sender=Signalement)
            try:
                instance.document = document_data
                if pdf_data:  # Only set PDF if conversion was successful
                    instance.pdf_document = pdf_data
                instance.document_generated_at = timezone.now()
                instance.save()
                logger.info(f"Documents saved for signalement {instance.id}")
            finally:
                post_save.connect(generate_document, sender=Signalement)
        except Exception as e:
            logger.error(f"Error generating document: {e}", exc_info=True)
