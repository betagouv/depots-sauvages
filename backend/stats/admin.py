from django.contrib import admin

from backend.stats.models import (
    StatsConstatation,
    StatsProConnectProfile,
    StatsSuiviProcedure,
    StatsUser,
)


@admin.register(StatsConstatation)
class StatsConstatationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "commune",
        "date_constat",
        "constatant_role",
        "auteur_identifie",
        "ceci_est_un_test",
        "user_hash",
        "created",
    ]
    list_filter = ["date_constat", "created", "auteur_identifie", "ceci_est_un_test"]
    search_fields = [
        "commune",
        "constatant_role",
        "user_hash",
    ]
    list_per_page = 25
    readonly_fields = [
        "created",
        "modified",
    ]


@admin.register(StatsSuiviProcedure)
class StatsSuiviProcedureAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "constatation",
        "etape_en_cours",
        "statut_traitement",
        "created",
    ]
    list_filter = [
        "etape_en_cours",
        "statut_traitement",
        "created",
    ]
    list_per_page = 25
    readonly_fields = [
        "created",
        "modified",
    ]


@admin.register(StatsUser)
class StatsUserAdmin(admin.ModelAdmin):
    list_display = ["id", "user_hash", "is_staff", "is_active", "date_joined", "last_login"]
    list_filter = ["is_staff", "is_active", "date_joined"]
    search_fields = ["user_hash"]
    list_per_page = 25


@admin.register(StatsProConnectProfile)
class StatsProConnectProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user_hash", "organization_label", "siret", "siren", "created", "modified"]
    list_filter = ["created", "modified"]
    search_fields = ["user_hash", "siret", "siren", "organization_label"]
    list_per_page = 25

