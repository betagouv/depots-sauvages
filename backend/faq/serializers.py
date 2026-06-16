from backend.guillotine.serializers import NestedBlockContentSerializer

from .models import FAQItem


class FAQItemSerializer(NestedBlockContentSerializer):
    class Meta(NestedBlockContentSerializer.Meta):
        model = FAQItem
