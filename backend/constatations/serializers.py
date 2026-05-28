from rest_framework import serializers

from .models import Constatation


class ConstatationSerializer(serializers.ModelSerializer):
    souhaite_porter_plainte = serializers.ReadOnlyField()

    class Meta:
        model = Constatation
        exclude = ["doc_constat", "lettre_info"]

    def get_docs_generation_flags(self, instance):
        return {
            "doc_constat_should_generate": True,
            "lettre_info_should_generate": bool(instance.auteur_identifie),
        }

    def update(self, instance, validated_data):
        validated_data.update(self.get_docs_generation_flags(instance))
        return super().update(instance, validated_data)

    def create(self, validated_data):
        validated_data.update(self.get_docs_generation_flags())
        return super().create(validated_data)
