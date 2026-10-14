import re

from backend.blog.models import BlogArticle
from backend.seo.utils import SITE_SUFFIX, clean_text, first_rich_text, truncate


def get_blog_seo_data(path: str) -> dict | None:
    """
    Checks if the path is a published blog article and returns its SEO metadata.
    """
    blog_match = re.match(r"^/blog/(?P<slug>[\w-]+)$", path)
    if not blog_match:
        return None
    article = BlogArticle.objects.published().filter(slug=blog_match.group("slug")).first()
    if not article:
        return None
    desc = clean_text(article.summary) or first_rich_text(article.content)
    return {
        "title": f"{article.title}{SITE_SUFFIX}",
        "desc": truncate(desc) if desc else None,
        "type": "article",
    }
