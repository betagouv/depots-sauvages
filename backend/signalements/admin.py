from django.contrib import admin

from .models import Signalement


@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display = [
        "commune",
        "date_constat",
        "created",
        "modified",
        "auteur_signalement",
        "doc_constat_generated_at",
        "lettre_info_generated_at",
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
    ]

    search_fields = [
        "commune",
        "localisation_depot",
        "auteur_signalement",
        "precisions_depot",
        "nom_entreprise",
        "nom_particulier",
        "prenom_particulier",
    ]

    readonly_fields = [
        "created",
        "modified",
        "doc_constat_generated_at",
        "lettre_info_generated_at",
    ]
