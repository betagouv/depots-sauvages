import re

from backend.blog.models import BlogArticle

SITE_NAME = "Stop Dépôt Sauvage"
TITLE_SUFFIX = f" - {SITE_NAME}"

# Google tronque les titres autour de 60-65 caractères et les descriptions autour
# de 155 : au-delà, le suffixe du site n'apporte rien et mange le titre de l'article.
MAX_TITLE_LENGTH = 65
MAX_DESCRIPTION_LENGTH = 155

BLOG_ARTICLE_PATH = re.compile(r"^/blog/(?P<slug>[\w-]+)$")


def _build_title(title: str) -> str:
    """Ajoute le nom du site au titre de l'article s'il reste assez de place."""
    title = " ".join(title.split())
    if len(title) + len(TITLE_SUFFIX) <= MAX_TITLE_LENGTH:
        return f"{title}{TITLE_SUFFIX}"
    return title


def _build_description(summary: str) -> str:
    """
    Normalise le chapô de l'article pour en faire une meta description.

    Les chapôs saisis contiennent des retours à la ligne et dépassent souvent la
    longueur affichée par les moteurs : on les aplatit et on tronque sur un mot.
    """
    description = " ".join((summary or "").split())
    if len(description) <= MAX_DESCRIPTION_LENGTH:
        return description
    truncated = description[: MAX_DESCRIPTION_LENGTH - 1]
    if " " in truncated:
        truncated = truncated.rsplit(" ", 1)[0]
    return f"{truncated.rstrip(',;:.')}…"


def get_blog_seo_data(path: str) -> dict | None:
    """
    Renvoie les métadonnées SEO d'un article de blog publié, ou None.

    Le titre et la description sont dérivés des champs déjà saisis (titre et
    chapô) : aucune ressaisie n'est demandée à la rédaction.
    """
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
