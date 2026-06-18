from rest_framework import serializers

from backend.constatations.models import Constatation


class UserSignalementSerializer(serializers.ModelSerializer):
    """Serializer for Constatation/user."""

    numero_dossier = serializers.IntegerField(source="id")
    date_creation = serializers.DateTimeField(source="created")
    date_modification = serializers.DateTimeField(source="modified")
    title = serializers.SerializerMethodField()

    class Meta:
        model = Constatation
        fields = [
            "id",
            "numero_dossier",
            "title",
            "date_creation",
            "date_modification",
            "date_constat",
            "heure_constat",
            "localisation_depot",
        ]

    def get_title(self, obj):
        return f"Procédure #{obj.id}"
