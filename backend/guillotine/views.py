from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response


class ReorderViewSetMixin:
    """
    Mixin for DRF ViewSets to enable up/down reordering of siblings.
    Assumes the model inherits from NestedContent (has parent and order fields).
    """

    @action(detail=True, methods=["post"], url_path="move-up")
    def move_up(self, request, pk=None):
        instance = self.get_object()
        moved = instance.move_up()
        result = "moved up" if moved else "no change"
        return Response({"result": result})

    @action(detail=True, methods=["post"], url_path="move-down")
    def move_down(self, request, pk=None):
        instance = self.get_object()
        moved = instance.move_down()
        result = "moved down" if moved else "no change"
        return Response({"result": result})


class NestedTopLevelListMixin:
    """
    Mixin to override the list action to return top-level nested items
    grouped into top-level categories and orphans.
    """

    def get_top_level_queryset(self, queryset):
        """
        Return the queryset of top-level items.
        Assumes is_top_level=True means the item is a top-level category/theme.
        """
        if hasattr(self.serializer_class.Meta.model, "is_top_level"):
            return queryset.filter(is_top_level=True)
        return queryset

    def get_orphans_queryset(self, queryset):
        """
        Return the queryset of top-level standalone/orphan items.
        Assumes is_top_level=False means the item is an orphan when parent is null.
        """
        if hasattr(self.serializer_class.Meta.model, "is_top_level"):
            return queryset.filter(is_top_level=False)
        return queryset.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(parent__isnull=True)
        top_level_qs = self.get_top_level_queryset(queryset)
        orphans_qs = self.get_orphans_queryset(queryset)
        # Get the ViewSet's configured serializer class
        serializer_class = self.get_serializer_class()

        class TopLevelResponseSerializer(serializers.Serializer):
            top_level = serializer_class(many=True)
            orphans = serializer_class(many=True)

        serializer = TopLevelResponseSerializer(
            {"top_level": top_level_qs, "orphans": orphans_qs},
            context=self.get_serializer_context(),
        )
        return Response(serializer.data)
