from html.parser import HTMLParser
from urllib.parse import urlparse

INTERNAL_HOSTS = {
    "depots-sauvages.beta.gouv.fr",
    "protect-envi.beta.gouv.fr",
    "localhost",
    "127.0.0.1",
}


def is_internal_url(url: str) -> bool:
    if not url:
        return False
    trimmed = url.strip()
    if (
        trimmed.startswith("/")
        or trimmed.startswith("#")
        or trimmed.startswith("mailto:")
        or trimmed.startswith("tel:")
    ):
        return True
    try:
        parsed = urlparse(trimmed)
        if not parsed.netloc:
            return True
        return parsed.hostname and parsed.hostname.lower() in INTERNAL_HOSTS
    except Exception:
        return False


def normalize_link_href(url: str) -> str:
    if not url:
        return ""
    trimmed = url.strip()
    try:
        parsed = urlparse(trimmed)
        if parsed.hostname and parsed.hostname.lower() in INTERNAL_HOSTS:
            path = parsed.path or "/"
            if parsed.query:
                path += "?" + parsed.query
            if parsed.fragment:
                path += "#" + parsed.fragment
            return path
    except Exception:
        pass
    return trimmed


class LinkCleaner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.result = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            attrs_dict = dict(attrs)
            href = attrs_dict.get("href", "")
            if is_internal_url(href):
                attrs_dict.pop("target", None)
                attrs_dict.pop("rel", None)
                attrs_dict["href"] = normalize_link_href(href)
            else:
                attrs_dict["target"] = "_blank"
                attrs_dict["rel"] = "noopener noreferrer"
            attrs_str = " ".join(f'{k}="{v}"' for k, v in attrs_dict.items())
            self.result.append(f"<{tag} {attrs_str}>" if attrs_str else f"<{tag}>")
        else:
            attrs_str = " ".join(f'{k}="{v}"' if v is not None else k for k, v in attrs)
            self.result.append(f"<{tag} {attrs_str}>" if attrs_str else f"<{tag}>")

    def handle_endtag(self, tag):
        self.result.append(f"</{tag}>")

    def handle_data(self, data):
        self.result.append(data)

    def handle_entityref(self, name):
        self.result.append(f"&{name};")

    def handle_charref(self, name):
        self.result.append(f"&#{name};")

    def clean(self, html_str: str) -> str:
        self.result = []
        self.feed(html_str)
        return "".join(self.result)


def clean_html_links(html_content: str) -> str:
    if not html_content or "<a" not in html_content:
        return html_content
    cleaner = LinkCleaner()
    return cleaner.clean(html_content)


def clean_blocks_content(blocks: list) -> tuple[list, bool]:
    if not isinstance(blocks, list):
        return blocks, False
    changed = False
    cleaned_blocks = []
    for block in blocks:
        if isinstance(block, dict) and block.get("type") == "rich_text" and "value" in block:
            original_val = block["value"]
            if isinstance(original_val, str) and "<a" in original_val:
                new_val = clean_html_links(original_val)
                if new_val != original_val:
                    changed = True
                    cleaned_blocks.append({**block, "value": new_val})
                    continue
        cleaned_blocks.append(block)
    return cleaned_blocks, changed
