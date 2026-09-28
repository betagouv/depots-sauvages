from rest_framework import serializers


class ProConnectAccessRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    organization_label = serializers.CharField(required=False, allow_blank=True, default="")
    siren = serializers.CharField(required=False, allow_blank=True, max_length=9, default="")
    siret = serializers.CharField(required=False, allow_blank=True, max_length=14, default="")
    name = serializers.CharField(required=False, allow_blank=True, default="")
    message = serializers.CharField(required=False, allow_blank=True, default="")

    def validate(self, attrs):
        siren = attrs.get("siren", "").strip()
        siret = attrs.get("siret", "").strip()
        organization_label = attrs.get("organization_label", "").strip()
        if not siren and len(siret) >= 9:
            attrs["siren"] = siret[:9]
        if not attrs.get("siren") and not siret and not organization_label:
            raise serializers.ValidationError(
                "Au moins un identifiant (SIREN, SIRET ou nom d'organisme) doit être fourni."
            )
        return attrs
