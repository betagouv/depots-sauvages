import logging

from django.forms.models import model_to_dict
from django.utils import timezone

from backend.doc_maker.odt import ODTProcessor

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
    today = timezone.now()
    context["today"] = today.strftime("%-d %B %Y")
    if context["date_constat"]:
        date_constat = context["date_constat"]
        context["date_constat"] = date_constat.strftime("%-d %B %Y")
    if context["heure_constat"]:
        heure_constat = context["heure_constat"]
        context["heure_constat"] = heure_constat.strftime("%H:%M")
    return context


def generate_document(instance, context, template_name):
    """
    Generate ODT document for the given instance and template.
    """
    processor = ODTProcessor()
    base_name = template_name.replace(".odt", "")
    return processor.process_template(
        template_name=template_name,
        context=context,
        output_filename=f"{base_name}-{instance.id}-{instance.commune}.odt",
    )


def generate_doc_constat(instance, context):
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
