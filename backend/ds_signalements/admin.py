from django.contrib import admin

from backend.ds_signalements.models import DSSignalement
from backend.signalements.admin import BaseSignalementAdminMixin

DS_SIGNALEMENTS_FIELDSETS = (
    (
        "Démarches Simplifiées",
        {
            "fields": (
                "ds_numero_dossier",
                "ds_date_depot",
                "ds_date_modification",
            )
        },
    ),
)


@admin.register(DSSignalement)
class DSSignalementAdmin(
    BaseSignalementAdminMixin,
    admin.ModelAdmin,
):
    list_display = ["ds_numero_dossier"] + BaseSignalementAdminMixin.list_display
    search_fields = ["ds_numero_dossier"] + BaseSignalementAdminMixin.search_fields
    readonly_fields = [
        # "ds_numero_dossier",
        "ds_date_depot",
        "ds_date_modification",
    ] + BaseSignalementAdminMixin.readonly_fields
    fieldsets = DS_SIGNALEMENTS_FIELDSETS + BaseSignalementAdminMixin.fieldsets
