from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """
    Serve Vue Application
    """

    template_name = "index.html"


index_view = never_cache(IndexView.as_view())
