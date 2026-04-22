from django.contrib import admin

from backend.procedures.models import SuiviProcedure


@admin.register(SuiviProcedure)
class SuiviProcedureAdmin(admin.ModelAdmin):
    list_display = ("signalement", "etape_en_cours", "created", "modified")
    list_filter = ("etape_en_cours", "decision_poursuite")
    search_fields = ("signalement__dn_numero_dossier",)
    readonly_fields = ("created", "modified")
    raw_id_fields = ("signalement",)

    fieldsets = (
        (
            None,
            {
                "fields": ("signalement", "etape_en_cours"),
            },
        ),
        (
            "Étape 1 : Pièces de procédure",
            {
                "fields": (
                    "preuves_fournies",
                    "constatation_signee",
                    "lettre_signe",
                ),
            },
        ),
        (
            "Étape 2 : Notification",
            {
                "fields": (
                    "lettre_envoyee",
                    "lettre_envoyee_date",
                    "copie_archives",
                    "ar_recu",
                    "ar_statut",
                    "ar_presentation_date",
                ),
            },
        ),
        (
            "Étape 3 & 4 : Décision et Actions",
            {
                "fields": (
                    "decision_poursuite",
                    "montant_fixe",
                    "montant_amende",
                    "arrete_redige",
                    "titre_recette_emis",
                    "notification_sanction_envoyee",
                    "motif_abandon_choisi",
                    "motif_abandon",
                    "souhaite_notifier_abandon",
                    "notification_abandon_envoyee",
                ),
            },
        ),
        (
            "Étape 5 : Clôture et Divers",
            {
                "fields": (
                    "nettoyage_fait",
                    "nettoyage_par",
                    "observations_internes",
                    "date_recouvrement_effective",
                    "titre_recette_confirme",
                    "montant_recouvre",
                    "dossier_archive",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created", "modified"),
                "classes": ("collapse",),
            },
        ),
    )
