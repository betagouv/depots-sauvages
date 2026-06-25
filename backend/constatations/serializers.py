from rest_framework import serializers

from backend.constatations.models import Constatation


class ConstatationSerializer(serializers.ModelSerializer):
    souhaite_porter_plainte = serializers.ReadOnlyField()
    numero_dossier = serializers.IntegerField(source="id", read_only=True)
    date_creation = serializers.DateTimeField(source="created", read_only=True)
    date_modification = serializers.DateTimeField(source="modified", read_only=True)

    class Meta:
        model = Constatation
        exclude = ["doc_constat", "lettre_info"]

    def get_docs_generation_flags(self, auteur_identifie):
        return {
            "doc_constat_should_generate": True,
            "lettre_info_should_generate": bool(auteur_identifie),
        }

    def update(self, instance, validated_data):
        auteur_identifie = validated_data.get("auteur_identifie", instance.auteur_identifie)
        validated_data.update(self.get_docs_generation_flags(auteur_identifie))
        return super().update(instance, validated_data)

    def create(self, validated_data):
        auteur_identifie = validated_data.get("auteur_identifie", False)
        validated_data.update(self.get_docs_generation_flags(auteur_identifie))
        return super().create(validated_data)
