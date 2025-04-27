from django.contrib import admin

from .models import Signalement


@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display = [
        "commune",
        "date_constat",
        "auteur_signalement",
        "nature_terrain",
        "volume_depot",
        "photo_dispo",
        "auteur_identifie",
        "statut_auteur",
        "document_generated_at",
    ]

    list_filter = [
        "commune",
        "date_constat",
        "nature_terrain",
        "photo_dispo",
        "auteur_identifie",
        "statut_auteur",
        "souhaite_porter_plainte",
        "arrete_municipal_existe",
        "prejudice_montant_connu",
        "generate_doc",
    ]

    search_fields = [
        "commune",
        "localisation_depot",
        "auteur_signalement",
        "precisions_depot",
        "precisions_indices",
        "nom_entreprise",
        "nom_particulier",
        "prenom_particulier",
        "numero_siret",
    ]
