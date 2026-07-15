from rest_framework import viewsets

from backend.guillotine.permissions import ReadOnlyOrAdminMutations

from .models import SiteContent
from .serializers import SiteContentSerializer


class SiteContentViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage editable site content.
    Anonymous users only see published items, while staff has full write access.
    """

    queryset = SiteContent.objects.all()
    serializer_class = SiteContentSerializer
    permission_classes = [ReadOnlyOrAdminMutations]
    lookup_field = "slug"

    def get_queryset(self):
        qs = SiteContent.objects.all()
        # Anonymous/non-staff users only see published items
        if not self.request.user or not self.request.user.is_staff:
            qs = qs.published()
        return qs
