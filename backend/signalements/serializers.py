"""Serializers for signalements app."""

from rest_framework import serializers

from backend.signalements.models import Signalement


class SignalementSerializer(serializers.ModelSerializer):
    """Serializer for Signalement model."""

    class Meta:
        model = Signalement
        exclude = [
            "doc_constat",
            "lettre_info",
            "prenom_particulier",
            "nom_particulier",
            "nom_entreprise",
            "numero_siret",
            "contact_nom",
            "contact_prenom",
            "contact_email",
            "contact_telephone",
            "auteur_signalement",
        ]
