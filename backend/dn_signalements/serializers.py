"""Serializers for signalements app."""

from rest_framework import serializers

from backend.dn_signalements.models import DNSignalement


class SignalementSerializer(serializers.ModelSerializer):
    """Serializer for Signalement model."""

    class Meta:
        model = DNSignalement
        exclude = [
            "doc_constat",
            "lettre_info",
            "constatant",
        ]
