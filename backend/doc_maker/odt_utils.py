import logging

from django.forms.models import model_to_dict

from backend.doc_maker.odt import ODTProcessor
from backend.doc_maker.settings import OUTPUT_DIR, TEMPLATE_DIR

logger = logging.getLogger(__name__)


def prepare_context(instance):
    """
    Prepare the context dictionary for document generation.
    """
    context = model_to_dict(instance)
    # Remove fields we don't need
    context.pop("id", None)
    context.pop("doc_constat_should_generate", None)
    context.pop("doc_constat", None)
    context.pop("doc_constat_generated_at", None)
    context["prejudice_montant_calcule"] = instance.get_prejudice_montant_calcule()
    # Format date and time fields
    if context["date_constat"]:
        context["date_constat"] = context["date_constat"].strftime("%d/%m/%Y")
    if context["heure_constat"]:
        context["heure_constat"] = context["heure_constat"].strftime("%H:%M")
    return context


def generate_odt_document(instance, context):
    """
    Generate an ODT document from the template and context.
    Returns the path to the generated ODT file.
    """
    logger.info(f"Generating ODT document for signalement {instance.id}")
    logger.debug(f"Template context: {context}")
    processor = ODTProcessor()  # This will ensure directories exist
    template_path = str(TEMPLATE_DIR / "template.odt")
    output_path = str(OUTPUT_DIR / f"signalement_{instance.id}.odt")
    generated_file_path = processor.process_template(
        template_path,
        context,
        output_path,
    )
    return generated_file_path


def read_odt_document(odt_path):
    """
    Read the contents of an ODT file.
    """
    with open(odt_path, "rb") as f:
        return f.read()
