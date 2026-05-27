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
    context["souhaite_porter_plainte"] = instance.souhaite_porter_plainte
    today = timezone.now()
    context["date_courante"] = today.strftime("%-d %B %Y")
    context["annee_courante"] = today.year
    date_constat = context.get("date_constat")
    heure_constat = context.get("heure_constat")
    if date_constat:
        context["date_constat"] = date_constat.strftime("%-d %B %Y")
    if heure_constat:
        context["heure_constat"] = heure_constat.strftime("%H:%M")
    role = context.get("constatant_role")
    if role:
        vowels = "aeiouyàâéèêëîïôûù"
        context["constatant_role_needs_elision"] = role[0].lower() in vowels
    c_pre = context.get("constatant_prenom") or ""
    c_nom = context.get("constatant_nom") or ""
    c_full = f"{c_pre} {c_nom}"
    context["constatant_nom_complet"] = c_full.replace("  ", " ").strip()
    a_civ = context.get("auteur_civilite") or ""
    a_pre = context.get("auteur_prenom") or ""
    a_nom = context.get("auteur_nom") or ""
    a_full = f"{a_civ} {a_pre} {a_nom}" if a_civ else f"{a_pre} {a_nom}"
    context["auteur_nom_complet"] = a_full.replace("  ", " ").strip()
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
