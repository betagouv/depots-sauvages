import logging
import re

from django.forms.models import model_to_dict
from django.utils import timezone

from backend.doc_maker.odt import ODTProcessor

logger = logging.getLogger(__name__)


class DocumentContextBuilder:
    """Builder class to prepare the context dictionary for ODT document generation."""

    def __init__(self, instance):
        self.instance = instance
        self.context = model_to_dict(instance)

    def remove_unneeded_fields(self):
        """Remove fields that are not needed in the ODT template context."""
        fields_to_remove = [
            "id",
            "doc_constat_should_generate",
            "doc_constat",
            "doc_constat_generated_at",
            "lettre_info_should_generate",
            "lettre_info",
            "lettre_info_generated_at",
        ]
        for field in fields_to_remove:
            self.context.pop(field, None)
        return self

    def add_calculated_fields(self):
        """Add custom calculated properties/methods from the instance."""
        self.context["prejudice_montant_calcule"] = self.instance.get_prejudice_montant_calcule()
        self.context["souhaite_porter_plainte"] = self.instance.souhaite_porter_plainte
        return self

    def add_current_date_info(self):
        """Add current date and year to the context."""
        today = timezone.now()
        self.context["date_courante"] = today.strftime("%-d %B %Y")
        self.context["annee_courante"] = today.year
        return self

    def format_constat_date_and_time(self):
        """Format the constatation date and time if present."""
        date_constat = self.context.get("date_constat")
        heure_constat = self.context.get("heure_constat")
        if date_constat:
            self.context["date_constat"] = date_constat.strftime("%-d %B %Y")
        if heure_constat:
            self.context["heure_constat"] = heure_constat.strftime("%H:%M")
        return self

    def check_constatant_role_elision(self):
        """Determine if the constatant role starts with a vowel, requiring elision (e.g., l'officier)."""
        role = self.context.get("constatant_role")
        if role:
            vowels = "aeiouyàâéèêëîïôûù"
            self.context["constatant_role_needs_elision"] = role[0].lower() in vowels
        return self

    def format_constatant_full_name(self):
        """Format the complete name of the constatant."""
        prenom = self.context.get("constatant_prenom") or ""
        nom = self.context.get("constatant_nom") or ""
        nom_complet = f"{prenom} {nom}"
        self.context["constatant_nom_complet"] = nom_complet.replace("  ", " ").strip()
        return self

    def format_auteur_adresse(self):
        """Split and format the auteur's address into two separate lines."""
        adresse = self.context.get("auteur_adresse") or ""
        adresse_ligne_1, adresse_ligne_2 = adresse, ""
        if adresse:
            if "\n" in adresse:
                parts = adresse.split("\n", 1)
                adresse_ligne_1 = parts[0].strip()
                adresse_ligne_2 = parts[1].strip()
            else:
                match = re.search(r"\s+(\d{5}\s+.*)$", adresse)
                if match:
                    position_postal_code = match.start()
                    adresse_ligne_1 = adresse[:position_postal_code].strip()
                    adresse_ligne_2 = match.group(1).strip()
        self.context["auteur_adresse_l1"] = adresse_ligne_1
        self.context["auteur_adresse_l2"] = adresse_ligne_2
        return self

    def format_auteur_full_name(self):
        """Format the complete name of the auteur, including civility if available."""
        civilite = self.context.get("auteur_civilite") or ""
        prenom = self.context.get("auteur_prenom") or ""
        nom = self.context.get("auteur_nom") or ""
        if civilite:
            nom_complet = f"{civilite} {prenom} {nom}"
        else:
            nom_complet = f"{prenom} {nom}"
        self.context["auteur_nom_complet"] = nom_complet.replace("  ", " ").strip()
        return self

    def build(self):
        """Build and return the final context dictionary."""
        self.remove_unneeded_fields()
        self.add_calculated_fields()
        self.add_current_date_info()
        self.format_constat_date_and_time()
        self.check_constatant_role_elision()
        self.format_constatant_full_name()
        self.format_auteur_adresse()
        self.format_auteur_full_name()
        return self.context


def prepare_context(instance):
    """
    Prepare the context dictionary for document generation.
    """
    return DocumentContextBuilder(instance).build()


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
