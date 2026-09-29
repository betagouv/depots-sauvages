import re

from backend.faq.models import FAQItem
from backend.seo.utils import excerpt_from_blocks, page_title


def get_faq_seo_data(path: str) -> dict | None:
    """
    Checks if the path is a dynamic FAQ page and returns its SEO title and description.
    """
    faq_match = re.match(r"^/faq/(?P<slug>[\w-]+)$", path)
    if not faq_match:
        return None
    faq_item = FAQItem.objects.filter(slug=faq_match.group("slug")).first()
    if not faq_item:
        return None
    return {
        "title": page_title(faq_item.title),
        "desc": excerpt_from_blocks(faq_item.content) or "Stop Dépôt Sauvage - Foire Aux Questions",
    }
