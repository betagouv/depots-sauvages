from rest_framework import viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from backend.guillotine.permissions import ReadOnlyOrAdminMutations
from backend.guillotine.views import ReorderViewSetMixin

from .models import BlogArticle
from .serializers import BlogArticleSerializer


class BlogArticleViewSet(ReorderViewSetMixin, viewsets.ModelViewSet):
    queryset = BlogArticle.objects.all()
    serializer_class = BlogArticleSerializer
    permission_classes = [ReadOnlyOrAdminMutations]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    lookup_field = "slug"

    def get_queryset(self):
        qs = BlogArticle.objects.all()
        if not self.request.user or not self.request.user.is_staff:
            qs = qs.published()
        return qs
