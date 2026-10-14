import re

from backend.blog.models import BlogArticle

SITE_NAME = "Stop Dépôt Sauvage"
TITLE_SUFFIX = f" - {SITE_NAME}"

# Search engines truncate titles around 60-65 chars and descriptions around 155 chars.
MAX_TITLE_LENGTH = 65
MAX_DESCRIPTION_LENGTH = 155

BLOG_ARTICLE_PATH = re.compile(r"^/blog/(?P<slug>[\w-]+)$")


def _build_title(title):
    """Appends site name to the article title if there is enough room."""
    title = " ".join(title.split())
    if len(title) + len(TITLE_SUFFIX) <= MAX_TITLE_LENGTH:
        return f"{title}{TITLE_SUFFIX}"
    return title


def _build_description(summary):
    """Normalizes the article summary into a clean meta description, flattened and truncated on a word boundary."""
    description = " ".join((summary or "").split())
    if len(description) <= MAX_DESCRIPTION_LENGTH:
        return description
    truncated = description[: MAX_DESCRIPTION_LENGTH - 1]
    if " " in truncated:
        truncated = truncated.rsplit(" ", 1)[0]
    return f"{truncated.rstrip(',;:.')}…"


def get_blog_seo_data(path):
    """Returns SEO metadata for a published blog article, or None."""
    match = BLOG_ARTICLE_PATH.match(path)
    if not match:
        return None
    try:
        article = BlogArticle.objects.published().filter(slug=match.group("slug")).first()
    except Exception:
        return None
    if not article:
        return None

    seo_data = {
        "title": _build_title(article.title),
        "desc": _build_description(article.summary),
        "og_type": "article",
        "published_time": article.created_at.isoformat() if article.created_at else None,
        "modified_time": article.updated_at.isoformat() if article.updated_at else None,
    }
    if article.cover_image:
        try:
            seo_data["image"] = article.cover_image.url
        except ValueError:
            pass
    return seo_data
