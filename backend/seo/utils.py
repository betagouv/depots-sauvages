import re

from django.utils.html import strip_tags

SITE_SUFFIX = " - Stop Dépôt Sauvage"
DESC_MAX_LENGTH = 150


def clean_text(text: str) -> str:
    """Removes HTML tags and collapses whitespace."""
    text = strip_tags(text or "").replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", text).strip()


def truncate(text: str, max_length: int = DESC_MAX_LENGTH) -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - 3].rsplit(" ", 1)[0] + "..."


def first_rich_text(content: list) -> str:
    """Returns the plain text of the first non-empty rich_text block."""
    for block in content or []:
        if block.get("type") == "rich_text" and block.get("value"):
            text = clean_text(block["value"])
            if text:
                return text
    return ""
