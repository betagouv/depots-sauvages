from rest_framework import viewsets

from backend.guillotine.permissions import ReadOnlyOrAdminMutations
from backend.guillotine.views import NestedTopLevelListMixin, ReorderViewSetMixin

from .models import FAQItem
from .serializers import FAQItemSerializer


class FAQItemViewSet(ReorderViewSetMixin, NestedTopLevelListMixin, viewsets.ModelViewSet):
    """
    ViewSet to manage FAQ items.
    Unauthenticated/non-staff users can only read published questions.
    """

    queryset = FAQItem.objects.all()
    serializer_class = FAQItemSerializer
    permission_classes = [ReadOnlyOrAdminMutations]

    def get_queryset(self):
        qs = FAQItem.objects.all()
        # Anonymous/non-staff users only see published questions
        if not self.request.user or not self.request.user.is_staff:
            qs = qs.published()
        return qs
