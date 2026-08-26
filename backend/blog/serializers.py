from rest_framework import serializers

from backend.guillotine.serializers import BlockContentSerializer

from .models import BlogArticle


class BlogArticleSerializer(BlockContentSerializer):
    slug = serializers.SlugField(required=False, allow_blank=True)
    cover_image = serializers.ImageField(required=False, allow_null=True)

    class Meta(BlockContentSerializer.Meta):
        model = BlogArticle
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "summary",
            "cover_image",
            "is_published",
            "order",
            "created_at",
            "updated_at",
        ]
