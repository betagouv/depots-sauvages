from django.contrib import admin

from backend.activity_logs.models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "created",
        "action",
        "actor",
        "target",
        "constatation",
        "suivi_procedure",
    ]
    list_filter = [
        "action",
        "target",
        "created",
    ]
    search_fields = [
        "action",
        "actor",
        "target",
        "description",
        "data",
    ]
    readonly_fields = [
        "created",
        "modified",
    ]
    raw_id_fields = (
        "constatation",
        "suivi_procedure",
    )
