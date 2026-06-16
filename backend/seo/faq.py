import re

from django.utils.html import strip_tags

from backend.faq.models import FAQItem


def get_faq_seo_data(path: str) -> dict | None:
    """
    Checks if the path is a dynamic FAQ page and returns its SEO title and description.
    """
    faq_match = re.match(r"^/faq/(?P<slug>[\w-]+)$", path)
    if not faq_match:
        return None
    slug = faq_match.group("slug")
    try:
        faq_item = FAQItem.objects.filter(slug=slug).first()
        if faq_item:
            desc = "Protect'Envi - Foire Aux Questions"
            for block in faq_item.content or []:
                if block.get("type") == "rich_text" and block.get("value"):
                    plain_text = strip_tags(block["value"])
                    plain_text = plain_text.replace("&nbsp;", " ").strip()
                    if len(plain_text) > 150:
                        desc = plain_text[:147] + "..."
                    else:
                        desc = plain_text
                    break
            return {
                "title": f"{faq_item.title} FAQ - Protect'Envi",
                "desc": desc,
            }
    except Exception:
        pass
    return None
