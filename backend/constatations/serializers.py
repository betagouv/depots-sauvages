from rest_framework import serializers

from .models import Constatation


class ConstatationSerializer(serializers.ModelSerializer):
    souhaite_porter_plainte = serializers.ReadOnlyField()

    class Meta:
        model = Constatation
        exclude = ["doc_constat", "lettre_info"]
