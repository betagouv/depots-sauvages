from rest_framework import serializers

from backend.proconnect.models import ProConnectAccessConfig


class ProConnectAccessRequestSerializer(serializers.Serializer):
    message = serializers.CharField(required=False, allow_blank=True, default="")


class CategorieJuridiqueItemSerializer(serializers.Serializer):
    code = serializers.RegexField(
        regex=r"^\d+$",
        max_length=10,
        error_messages={"invalid": "Le code doit contenir uniquement des chiffres."},
    )
    nom = serializers.CharField(required=False, allow_blank=True, max_length=255, default="")

    def validate_code(self, value):
        return value.strip()

    def validate_nom(self, value):
        return value.strip()


class SirenItemSerializer(serializers.Serializer):
    siren = serializers.CharField(max_length=9)
    nom = serializers.CharField(required=False, allow_blank=True, max_length=255, default="")

    def validate_siren(self, value):
        siren = value.strip().replace(" ", "")
        if len(siren) != 9 or not siren.isdigit():
            raise serializers.ValidationError("Le SIREN doit comporter exactement 9 chiffres.")
        return siren

    def validate_nom(self, value):
        return value.strip()


class ProConnectAccessConfigSerializer(serializers.ModelSerializer):
    categories_juridiques_autorisees = serializers.ListField(
        child=CategorieJuridiqueItemSerializer(),
        required=False,
    )
    sirens_autorises = serializers.ListField(
        child=SirenItemSerializer(),
        required=False,
    )

    class Meta:
        model = ProConnectAccessConfig
        fields = [
            "categories_juridiques_autorisees",
            "sirens_autorises",
        ]

    def validate_sirens_autorises(self, value):
        seen_sirens = set()
        duplicates = set()
        for item in value:
            siren = item.get("siren")
            if siren in seen_sirens:
                duplicates.add(siren)
            seen_sirens.add(siren)
        if duplicates:
            raise serializers.ValidationError(
                f"Le(s) SIREN suivant(s) apparaisse(nt) en double : {', '.join(sorted(duplicates))}."
            )
        return value

    def validate_categories_juridiques_autorisees(self, value):
        seen_codes = set()
        duplicates = set()
        for item in value:
            code = item.get("code")
            if code in seen_codes:
                duplicates.add(code)
            seen_codes.add(code)
        if duplicates:
            raise serializers.ValidationError(
                f"Le(s) code(s) suivant(s) apparaisse(nt) en double : {', '.join(sorted(duplicates))}."
            )
        return value
