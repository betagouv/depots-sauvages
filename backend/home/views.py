from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from backend.seo.seo_metadata import build_seo_context


class IndexView(TemplateView):
    """
    Serve Vue Application
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(build_seo_context(self.request.path))
        return context


index_view = never_cache(IndexView.as_view())
