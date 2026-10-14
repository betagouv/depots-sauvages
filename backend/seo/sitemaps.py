from dataclasses import dataclass
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.sitemaps import Sitemap

from backend.blog.models import BlogArticle
from backend.faq.models import FAQItem

# Stable public pages intended for search engine indexing.
STATIC_PUBLIC_PATHS = [
    ("/", 1.0),
    ("/comment-agir", 0.8),
    ("/comprendre-la-procedure", 0.8),
    ("/blog", 0.8),
    ("/faq", 0.7),
    ("/simulateur", 0.7),
    ("/calculateur", 0.7),
    ("/rdv", 0.6),
    ("/demarche-numerique-rejoindre-stop-depot-sauvage", 0.6),
    ("/contact", 0.5),
]


@dataclass
class _PublicSite:
    """Public domain as configured in settings."""

    domain: str


class BaseSiteSitemap(Sitemap):
    """
    Sitemap built on top of SITE_BASE_URL rather than the requested domain,
    ensuring consistent absolute URLs across aliases and domains.
    """

    protocol = "https"

    def get_urls(self, page=1, site=None, protocol=None):
        parsed = urlparse(settings.SITE_BASE_URL)
        if parsed.netloc:
            site = _PublicSite(domain=parsed.netloc)
            protocol = parsed.scheme or self.protocol
        return super().get_urls(page=page, site=site, protocol=protocol)


class StaticViewSitemap(BaseSiteSitemap):
    changefreq = "monthly"

    def items(self):
        return STATIC_PUBLIC_PATHS

    def location(self, item):
        return item[0]

    def priority(self, item):
        return item[1]


class BlogSitemap(BaseSiteSitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return BlogArticle.objects.published().order_by("order", "id")

    def location(self, article):
        return f"/blog/{article.slug}"

    def lastmod(self, article):
        return article.updated_at


class FAQSitemap(BaseSiteSitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return (
            FAQItem.objects.published().exclude(slug="").exclude(slug=None).order_by("order", "id")
        )

    def location(self, item):
        return f"/faq/{item.slug}"

    def lastmod(self, item):
        return item.updated_at


SITEMAPS = {
    "pages": StaticViewSitemap,
    "blog": BlogSitemap,
    "faq": FAQSitemap,
}
