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
    context.pop("lettre_info_should_generate", None)
    context.pop("lettre_info", None)
    context.pop("lettre_info_generated_at", None)
    context["prejudice_montant_calcule"] = instance.get_prejudice_montant_calcule()
    # Format date and time fields
    if context["date_constat"]:
        context["date_constat"] = context["date_constat"].strftime("%d/%m/%Y")
    if context["heure_constat"]:
        context["heure_constat"] = context["heure_constat"].strftime("%H:%M")
    return context


def generate_document(instance, context, template_name):
    """
    Generate ODT document for the given instance and template.
    """
    processor = ODTProcessor()
    base_name = template_name.replace(".odt", "")
    return processor.generate_document(
        template_path=TEMPLATE_DIR / template_name,
        output_dir=OUTPUT_DIR,
        context=context,
        filename=f"{base_name}-{instance.id}-{instance.commune}",
    )


def generate_odt_document(instance, context):
    """
    Generate 'rapport de constatation' ODT document.
    """
    return generate_document(instance, context, template_name="doc-constat.odt")


def generate_lettre_info(instance, context):
    """
    Generate 'lettre info' ODT document.
    """
    return generate_document(instance, context, template_name="lettre-info.odt")


def read_odt_document(file_path):
    """
    Read ODT document from file.
    """
    with open(file_path, "rb") as f:
        return f.read()
