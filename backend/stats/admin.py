from django.contrib import admin

from backend.stats.models import ExternalMetric, StatsConstatation, StatsSuiviProcedure


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


@admin.register(ExternalMetric)
class ExternalMetricAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "source",
        "metric",
        "dimension",
        "value",
        "collected_at",
    ]
    list_filter = ["source", "metric", "date"]
    search_fields = ["metric", "dimension"]
    date_hierarchy = "date"
    list_per_page = 50
    readonly_fields = ["collected_at"]


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
