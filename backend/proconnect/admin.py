from django.contrib import admin

from backend.proconnect.models import ProConnectProfile


@admin.register(ProConnectProfile)
class ProConnectProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "organization_label", "siret", "siren", "roles", "modified")
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "siret",
        "siren",
        "organization_label",
    )
    readonly_fields = ("created", "modified")
