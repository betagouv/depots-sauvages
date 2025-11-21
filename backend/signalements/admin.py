from django.contrib import admin

from .models import Signalement


class BaseSignalementAdminMixin:
    list_display = [
        "commune",
        "date_constat",
        "auteur_signalement",
        "auteur_identifie",
        "souhaite_porter_plainte",
        "contact_nom",
        "contact_prenom",
        "accepte_accompagnement",
        "created",
        "modified",
    ]
    list_filter = [
        "date_constat",
        "created",
        "modified",
        "doc_constat_generated_at",
        "lettre_info_generated_at",
        "nature_terrain",
        "photo_dispo",
        "auteur_identifie",
        "statut_auteur",
        "accepte_accompagnement",
    ]
    search_fields = [
        "commune",
        "localisation_depot",
        "auteur_signalement",
        "precisions_depot",
        "nom_entreprise",
        "nom_particulier",
        "prenom_particulier",
        "contact_nom",
        "contact_prenom",
        "contact_email",
    ]
    readonly_fields = [
        "created",
        "modified",
        "doc_constat_generated_at",
        "lettre_info_generated_at",
    ]
    fieldsets = (
        (
            "Information générale",
            {
                "fields": (
                    "commune",
                    "date_constat",
                    "heure_constat",
                    "auteur_signalement",
                )
            },
        ),
        (
            "Localisation et description",
            {
                "fields": (
                    "localisation_depot",
                    "nature_terrain",
                    "volume_depot",
                    "risque_ecoulement",
                    "types_depot",
                    "precisions_depot",
                    "photo_dispo",
                )
            },
        ),
        (
            "Auteur du dépôt et procédure",
            {
                "fields": (
                    "auteur_identifie",
                    "statut_auteur",
                    "nom_entreprise",
                    "numero_siret",
                    "nom_particulier",
                    "prenom_particulier",
                    "souhaite_porter_plainte",
                    "indices_disponibles",
                    "precisions_indices",
                    "arrete_municipal_existe",
                    "montant_forfait_enlevement",
                )
            },
        ),
        (
            "Contact",
            {
                "fields": (
                    "contact_nom",
                    "contact_prenom",
                    "contact_email",
                    "contact_telephone",
                    "accepte_accompagnement",
                )
            },
        ),
        (
            "Préjudice",
            {
                "fields": (
                    "prejudice_montant_connu",
                    "prejudice_montant",
                    "prejudice_nombre_personnes",
                    "prejudice_nombre_heures",
                    "prejudice_nombre_vehicules",
                    "prejudice_kilometrage",
                    "prejudice_autres_couts",
                )
            },
        ),
        (
            "Documents",
            {
                "fields": (
                    "doc_constat_should_generate",
                    "doc_constat_generated_at",
                    "lettre_info_should_generate",
                    "lettre_info_generated_at",
                )
            },
        ),
        (
            "Métadonnées",
            {
                "fields": (
                    "created",
                    "modified",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Signalement)
class SignalementAdmin(
    BaseSignalementAdminMixin,
    admin.ModelAdmin,
):
    pass
