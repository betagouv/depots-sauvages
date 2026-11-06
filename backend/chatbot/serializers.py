from rest_framework import serializers
from backend.chatbot.models import ChatbotConfig, DEFAULT_SYSTEM_PROMPT


class ChatbotConfigSerializer(serializers.ModelSerializer):
    # Champ calculé indiquant si une clé est configurée (sans exposer la clé complète)
    has_api_key = serializers.SerializerMethodField()
    api_key_masked = serializers.SerializerMethodField()
    default_system_prompt = serializers.SerializerMethodField()

    class Meta:
        model = ChatbotConfig
        fields = [
            "id",
            "provider",
            "model",
            "api_key",
            "base_url",
            "timeout",
            "system_prompt",
            "has_api_key",
            "api_key_masked",
            "default_system_prompt",
        ]
        extra_kwargs = {
            "api_key": {"write_only": True, "required": False, "allow_blank": True},
        }

    def get_has_api_key(self, obj) -> bool:
        return bool(obj.api_key and obj.api_key.strip())

    def get_api_key_masked(self, obj) -> str:
        key = (obj.api_key or "").strip()
        if not key:
            return ""
        if len(key) <= 8:
            return "••••••••"
        return f"{key[:4]}••••••••{key[-4:]}"

    def get_default_system_prompt(self, obj) -> str:
        return DEFAULT_SYSTEM_PROMPT

    def update(self, instance, validated_data):
        # Si la clé n'est pas passée ou laissée vide alors qu'il y en avait déjà une et qu'on ne veut pas l'écraser :
        # Note: si on transmet "" expressément, on autorise le reset de la clé.
        return super().update(instance, validated_data)
