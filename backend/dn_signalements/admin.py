from django.contrib import admin

from backend.dn_signalements.models import DNSignalement
from backend.signalements.admin import BaseSignalementAdminMixin


DN_SIGNALEMENTS_FIELDSETS = (
    (
        "Démarche Numérique",
        {
            "fields": (
                "user",
                "dn_numero_dossier",
                "dn_date_creation",
                "dn_date_modification",
            )
        },
    ),
)


@admin.register(DNSignalement)
class DNSignalementAdmin(
    BaseSignalementAdminMixin,
    admin.ModelAdmin,
):
    list_display = ["dn_numero_dossier", "user"] + BaseSignalementAdminMixin.list_display
    search_fields = ["dn_numero_dossier", "user__email"] + BaseSignalementAdminMixin.search_fields
    readonly_fields = [
        "dn_numero_dossier",
        "dn_date_creation",
        "dn_date_modification",
    ] + BaseSignalementAdminMixin.readonly_fields
    fieldsets = DN_SIGNALEMENTS_FIELDSETS + BaseSignalementAdminMixin.fieldsets

