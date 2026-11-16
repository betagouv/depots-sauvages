from django.contrib import admin

from .models import Team, TeamAutoCreationExclusion


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "siret", "siren", "created", "modified")
    search_fields = ("name", "siret", "siren")
    readonly_fields = ("created", "modified")


@admin.register(TeamAutoCreationExclusion)
class TeamAutoCreationExclusionAdmin(admin.ModelAdmin):
    list_display = ("label", "siren", "siret", "created", "modified")
    search_fields = ("label", "siren", "siret", "reason")
    readonly_fields = ("created", "modified")
