"""Serializers for signalements app."""

from rest_framework import serializers

from backend.dn_signalements.models import DNSignalement


class UserSignalementSerializer(serializers.ModelSerializer):
    """Serializer for Signalement/user."""

    numero_dossier = serializers.IntegerField(source="dn_numero_dossier")
    date_creation = serializers.DateTimeField(source="dn_date_creation")
    date_modification = serializers.DateTimeField(source="dn_date_modification")

    class Meta:
        model = DNSignalement
        fields = [
            "id",
            "numero_dossier",
            "title",
            "date_creation",
            "date_modification",
            "date_constat",
            "localisation_depot",
        ]
