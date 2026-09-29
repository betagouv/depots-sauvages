from django.utils.html import strip_tags

SITE_NAME = "Stop Dépôt Sauvage"


def page_title(title: str) -> str:
    return f"{title} - {SITE_NAME}"


def excerpt_from_blocks(content, max_length: int = 150) -> str | None:
    """
    Returns the plain text of the first rich text block, truncated to max_length.
    """
    for block in content or []:
        if block.get("type") == "rich_text" and block.get("value"):
            plain_text = strip_tags(block["value"]).replace("&nbsp;", " ").strip()
            if len(plain_text) > max_length:
                return plain_text[: max_length - 3] + "..."
            return plain_text
    return None
