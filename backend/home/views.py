import json
from urllib.parse import urljoin

from django.conf import settings
from django.utils.safestring import mark_safe
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from backend.seo.seo_metadata import get_seo_data, is_private_path, normalize_path

DEFAULT_TITLE = (
    "Stop Dépôt Sauvage - Accompagner les collectivités pour mieux lutter contre "
    "les dépôts sauvages."
)
DEFAULT_DESCRIPTION = "Signaler un dépôt sauvage avec Stop Dépôt Sauvage."
SITE_NAME = "Stop Dépôt Sauvage"


def absolute_url(path_or_url):
    """Complète une adresse relative avec le domaine public du site."""
    if not path_or_url:
        return None
    if path_or_url.startswith(("http://", "https://")):
        return path_or_url
    return urljoin(settings.SITE_BASE_URL.rstrip("/") + "/", path_or_url.lstrip("/"))


def build_article_jsonld(seo_data, canonical, image):
    """
    Décrit un article de blog au format schema.org, pour que les moteurs sachent
    qu'il s'agit d'un article daté et non d'une page quelconque.
    """
    jsonld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": seo_data.get("title"),
        "description": seo_data.get("desc"),
        "mainEntityOfPage": canonical,
        "url": canonical,
        "inLanguage": "fr-FR",
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": settings.SITE_BASE_URL,
        },
    }
    if image:
        jsonld["image"] = image
    if seo_data.get("published_time"):
        jsonld["datePublished"] = seo_data["published_time"]
    if seo_data.get("modified_time"):
        jsonld["dateModified"] = seo_data["modified_time"]
    return jsonld


class IndexView(TemplateView):
    """
    Serve Vue Application
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path = self.request.path
        seo_data = get_seo_data(path) or {}

        context["seo_title"] = seo_data.get("title") or DEFAULT_TITLE
        context["seo_description"] = seo_data.get("desc") or DEFAULT_DESCRIPTION
        context["seo_site_name"] = SITE_NAME

        is_prod = getattr(settings, "ENV_NAME", "") == "prod"
        context["seo_robots"] = (
            "index, follow" if is_prod and not is_private_path(path) else "noindex, nofollow"
        )

        canonical = absolute_url(normalize_path(path))
        context["seo_canonical"] = canonical
        context["seo_og_type"] = seo_data.get("og_type", "website")

        image = absolute_url(seo_data.get("image") or settings.SEO_DEFAULT_IMAGE)
        context["seo_image"] = image

        if seo_data.get("og_type") == "article":
            context["seo_published_time"] = seo_data.get("published_time")
            context["seo_modified_time"] = seo_data.get("modified_time")
            jsonld = build_article_jsonld(seo_data, canonical, image)
            # `</script>` dans une chaîne fermerait la balise : on l'échappe.
            context["seo_jsonld"] = mark_safe(
                json.dumps(jsonld, ensure_ascii=False).replace("<", "\\u003C")
            )

        return context


index_view = never_cache(IndexView.as_view())
