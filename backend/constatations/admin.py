from django.contrib import admin

from backend.constatations.models import Constatation


@admin.register(Constatation)
class ConstatationAdmin(admin.ModelAdmin):
    list_display = [
        "commune",
        "date_constat",
        "constatant_role",
        "user",
        "auteur_identifie",
        "contact_nom",
        "contact_prenom",
        "accepte_accompagnement",
        "ceci_est_un_test",
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
        "risque_ecoulement",
        "auteur_identifie",
        "statut_auteur",
        "accepte_accompagnement",
        "ceci_est_un_test",
    ]
    search_fields = [
        "commune",
        "localisation_depot",
        "constatant_role",
        "constatant_nom",
        "constatant_prenom",
        "precisions_depot",
        "contact_nom",
        "contact_prenom",
        "contact_email",
        "user__email",
        "user__username",
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
                    "user",
                    "commune",
                    "date_constat",
                    "heure_constat",
                    "constatant_role",
                    "constatant_civilite",
                    "constatant_prenom",
                    "constatant_nom",
                    "constatant_est_utilisateur_connecte",
                    "ceci_est_un_test",
                )
            },
        ),
        (
            "Localisation et description",
            {
                "fields": (
                    "localisation_depot",
                    "nature_terrain",
                    "proprietaire_terrain_prive",
                    "volume_depot",
                    "types_depot",
                    "precisions_depot",
                    "photo_dispo",
                    "risque_ecoulement",
                )
            },
        ),
        (
            "Auteur du dépôt et procédure",
            {
                "fields": (
                    "auteur_identifie",
                    "statut_auteur",
                    "auteur_civilite",
                    "auteur_nom",
                    "auteur_prenom",
                    "auteur_adresse",
                    "auteur_siret",
                    "entreprise_francaise",
                    "informations_auteur",
                    "plainte_etat",
                    "indices_disponibles",
                    "precisions_indices",
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
