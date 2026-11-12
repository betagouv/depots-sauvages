from rest_framework import serializers
from backend.chatbot.models import ChatbotConfig, ChatbotConversation, get_default_system_prompt


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

    def get_has_api_key(self, obj):
        return bool(obj.api_key and obj.api_key.strip())

    def get_api_key_masked(self, obj):
        key = (obj.api_key or "").strip()
        if not key:
            return ""
        if len(key) <= 8:
            return "••••••••"
        return f"{key[:4]}••••••••{key[-4:]}"

    def get_default_system_prompt(self, obj):
        return get_default_system_prompt()

    def update(self, instance, validated_data):
        # Si la clé n'est pas passée ou laissée vide alors qu'il y en avait déjà une et qu'on ne veut pas l'écraser :
        # Note: si on transmet "" expressément, on autorise le reset de la clé.
        return super().update(instance, validated_data)


class ChatbotConversationListSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    messages_count = serializers.SerializerMethodField()
    first_user_message = serializers.SerializerMethodField()
    last_user_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatbotConversation
        fields = [
            "id",
            "user_email",
            "user_name",
            "current_path",
            "messages_count",
            "first_user_message",
            "last_user_message",
            "has_draft_proposed",
            "feedback",
            "created_at",
            "updated_at",
        ]

    def get_user_email(self, obj):
        if obj.user and getattr(obj.user, "email", None):
            return obj.user.email
        return "Utilisateur supprimé"

    def get_user_name(self, obj):
        if not obj.user:
            return ""
        full = f"{getattr(obj.user, 'first_name', '')} {getattr(obj.user, 'last_name', '')}".strip()
        return full

    def get_messages_count(self, obj):
        if isinstance(obj.messages, list):
            return len(obj.messages)
        return 0

    def get_first_user_message(self, obj):
        if not isinstance(obj.messages, list):
            return ""
        for msg in obj.messages:
            if isinstance(msg, dict) and msg.get("role") == "user" and msg.get("content"):
                return str(msg.get("content"))[:200]
        return ""

    def get_last_user_message(self, obj):
        if not isinstance(obj.messages, list):
            return ""
        for msg in reversed(obj.messages):
            if isinstance(msg, dict) and msg.get("role") == "user" and msg.get("content"):
                return str(msg.get("content"))[:200]
        return ""


class ChatbotConversationDetailSerializer(ChatbotConversationListSerializer):
    class Meta(ChatbotConversationListSerializer.Meta):
        fields = ChatbotConversationListSerializer.Meta.fields + ["messages"]

