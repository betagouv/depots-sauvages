import re

from backend.faq.models import FAQItem
from backend.seo.utils import SITE_SUFFIX, first_rich_text, truncate


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
    desc = first_rich_text(faq_item.content)
    return {
        "title": f"{faq_item.title}{SITE_SUFFIX}",
        "desc": truncate(desc) if desc else "Stop Dépôt Sauvage - Foire Aux Questions",
    }
