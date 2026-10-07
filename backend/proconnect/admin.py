from django.contrib import admin
from solo.admin import SingletonModelAdmin

from backend.proconnect.models import ProConnectAccessConfig, ProConnectProfile, PublicEntitySirene


@admin.register(ProConnectAccessConfig)
class ProConnectAccessConfigAdmin(SingletonModelAdmin):
    fieldsets = (
        (
            "Règles d'accès",
            {
                "fields": (
                    "categories_juridiques_autorisees",
                    "sirens_autorises",
                ),
                "description": (
                    "Configuration des catégories juridiques des collectivités (avec préfixes et libellés) "
                    "et des SIREN spécifiques autorisés (Gendarmerie, ONF, OFB, dérogations)."
                ),
            },
        ),
    )


@admin.register(ProConnectProfile)
class ProConnectProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "organization_label", "siret", "siren", "roles", "modified")
    raw_id_fields = ("user",)
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "siret",
        "siren",
        "organization_label",
    )
    readonly_fields = ("created", "modified", "user")


@admin.register(PublicEntitySirene)
class PublicEntitySireneAdmin(admin.ModelAdmin):
    list_display = ("siren", "categorie_juridique", "denomination", "modified")
    search_fields = ("siren", "denomination", "categorie_juridique")
    list_filter = ("categorie_juridique",)
    readonly_fields = ("created", "modified")
