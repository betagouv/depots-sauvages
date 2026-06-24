from django.conf import settings
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from backend.seo.seo_metadata import get_seo_data


class IndexView(TemplateView):
    """
    Serve Vue Application
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seo_data = get_seo_data(self.request.path) or {}
        context["seo_title"] = (
            seo_data.get("title")
            or "Protect’Envi - Accompagner les collectivités pour mieux lutter contre les dépôts sauvages."
        )
        context["seo_description"] = (
            seo_data.get("desc") or "Signaler un dépôt sauvage avec Protect'Envi."
        )
        context["seo_robots"] = (
            "noindex, nofollow" if getattr(settings, "ENV_NAME", "") != "prod" else "index, follow"
        )
        return context


index_view = never_cache(IndexView.as_view())
