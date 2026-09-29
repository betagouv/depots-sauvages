import re

from backend.blog.models import BlogArticle
from backend.seo.utils import excerpt_from_blocks, page_title


def get_blog_seo_data(path: str) -> dict | None:
    """
    Checks if the path is a published blog article and returns its SEO data.
    """
    blog_match = re.match(r"^/blog/(?P<slug>[\w-]+)$", path)
    if not blog_match:
        return None
    article = BlogArticle.objects.published().filter(slug=blog_match.group("slug")).first()
    if not article:
        return None
    return {
        "title": page_title(article.title),
        "desc": article.summary.strip()
        or excerpt_from_blocks(article.content)
        or "Retour d'expérience Stop Dépôt Sauvage.",
        "image": article.cover_image.url if article.cover_image else None,
        "type": "article",
    }
