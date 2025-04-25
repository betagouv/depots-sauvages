import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.utils import timezone
from python_odt_template.libreoffice import libreoffice

from backend.doc_maker.odt import ODTProcessor
from backend.doc_maker.settings import OUTPUT_DIR, TEMPLATE_DIR
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

            # Define output paths
            odt_filename = f"signalement_{instance.id}.odt"
            pdf_filename = f"signalement_{instance.id}.pdf"
            output_odt_path = OUTPUT_DIR / odt_filename
            output_pdf_path = OUTPUT_DIR / pdf_filename
            # Generate ODT document
            processor = ODTProcessor()  # This will ensure directories exist
            output_odt_path = processor.process_template(
                str(TEMPLATE_DIR / "template.odt"),
                context,
                str(output_odt_path),
            )
            # Convert to PDF using the library's function
            libreoffice.convert(str(output_odt_path), str(OUTPUT_DIR))

            # Check if conversion was successful
            if not output_pdf_path.exists():
                logger.error(
                    f"PDF conversion failed - LibreOffice did not generate {output_pdf_path}"
                )
                logger.debug(f"ODT file exists: {output_odt_path.exists()}")
                logger.debug(f"Directory contents: {list(OUTPUT_DIR.glob('*'))}")
                raise RuntimeError(
                    "PDF conversion failed - LibreOffice did not generate the PDF file"
                )

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
