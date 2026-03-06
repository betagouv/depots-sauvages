from django.contrib import admin

from backend.dn_signalements.models import DNSignalement, UserDossier
from backend.signalements.admin import BaseSignalementAdminMixin, ReadOnlyMixin

DN_SIGNALEMENTS_FIELDSETS = (
    (
        "Démarche Numérique",
        {
            "fields": (
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
    list_display = ["dn_numero_dossier"] + BaseSignalementAdminMixin.list_display
    search_fields = ["dn_numero_dossier"] + BaseSignalementAdminMixin.search_fields
    readonly_fields = [
        "dn_numero_dossier",
        "dn_date_creation",
        "dn_date_modification",
    ] + BaseSignalementAdminMixin.readonly_fields
    fieldsets = DN_SIGNALEMENTS_FIELDSETS + BaseSignalementAdminMixin.fieldsets


@admin.register(UserDossier)
class UserDossierAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = (
        "numero_dossier",
        "user",
        "date_creation",
        "date_modification",
        "date_constat",
        "localisation_depot",
    )
    search_fields = ["numero_dossier", "user__email", "user__username"]
    list_filter = ["date_creation", "date_modification", "date_constat"]
