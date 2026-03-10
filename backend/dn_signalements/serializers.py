"""Serializers for signalements app."""

from rest_framework import serializers

from backend.dn_signalements.models import DNSignalement, UserDossier


class SignalementSerializer(serializers.ModelSerializer):
    """Serializer for Signalement model."""

    class Meta:
        model = DNSignalement
        exclude = [
            "doc_constat",
            "lettre_info",
            "constatant",
        ]


class UserDossierSerializer(serializers.ModelSerializer):
    """Serializer for UserDossier model."""

    class Meta:
        model = UserDossier
        fields = [
            "id",
            "numero_dossier",
            "title",
            "date_creation",
            "date_modification",
            "date_constat",
            "localisation_depot",
        ]
