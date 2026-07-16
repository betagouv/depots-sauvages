from backend.guillotine.serializers import BlockContentSerializer

from .models import SiteContent


class SiteContentSerializer(BlockContentSerializer):
    class Meta(BlockContentSerializer.Meta):
        model = SiteContent
        fields = ["id", "title", "content", "slug", "is_published"]
