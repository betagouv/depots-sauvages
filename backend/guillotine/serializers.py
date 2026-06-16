from rest_framework import serializers


class BlockContentSerializerMixin(serializers.Serializer):
    """
    Serializer mixin for models inheriting from BlockContent.
    Exposes content directly as JSON.
    """

    content = serializers.JSONField(required=False)


class NestedContentSerializerMixin(serializers.Serializer):
    """
    Serializer mixin for models inheriting from NestedContent.
    Exposes recursive hierarchy of children.
    """

    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        request = self.context.get("request")
        is_staff = request and request.user and request.user.is_staff
        # Only serialize children if this is a top-level node
        if obj.parent_id is not None:
            return []
        qs = obj.children.all()
        if not is_staff:
            qs = qs.published()
        serializer_class = self.__class__
        return serializer_class(qs, many=True, context=self.context).data


class BlockContentSerializer(BlockContentSerializerMixin, serializers.ModelSerializer):
    """Base model serializer for models inheriting from BlockContent."""

    class Meta:
        fields = ["id", "title", "content", "slug", "is_published", "created_at", "updated_at"]


class NestedBlockContentSerializer(
    BlockContentSerializerMixin,
    NestedContentSerializerMixin,
    serializers.ModelSerializer,
):
    """Base model serializer for models inheriting from both BlockContent and NestedContent."""

    class Meta:
        fields = [
            "id",
            "title",
            "content",
            "slug",
            "is_published",
            "parent",
            "order",
            "children",
            "is_top_level",
            "created_at",
            "updated_at",
        ]
