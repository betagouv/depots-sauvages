import pytest

from backend.guillotine.link_utils import (
    clean_blocks_content,
    clean_html_links,
    is_internal_url,
    normalize_link_href,
)


def test_is_internal_url():
    assert is_internal_url("/") is True
    assert is_internal_url("/calculateur") is True
    assert is_internal_url("#anchor") is True
    assert is_internal_url("mailto:test@example.com") is True
    assert is_internal_url("https://protect-envi.beta.gouv.fr/calculateur") is True
    assert is_internal_url("https://depots-sauvages.beta.gouv.fr/contact") is True
    assert is_internal_url("http://localhost:5173/page") is True
    assert is_internal_url("http://127.0.0.1:8000/api") is True
    assert is_internal_url("https://www.legifrance.gouv.fr/codes/article") is False
    assert is_internal_url("https://google.com") is False


def test_normalize_link_href():
    assert normalize_link_href("https://protect-envi.beta.gouv.fr/calculateur") == "/calculateur"
    assert (
        normalize_link_href(
            "https://protect-envi.beta.gouv.fr/demarrer-constatation?foo=bar#section"
        )
        == "/demarrer-constatation?foo=bar#section"
    )
    assert normalize_link_href("/already-relative") == "/already-relative"
    assert (
        normalize_link_href("https://www.legifrance.gouv.fr/codes/article")
        == "https://www.legifrance.gouv.fr/codes/article"
    )


def test_clean_html_links():
    html_input = (
        '<p><a target="_blank" rel="noopener noreferrer nofollow" class="fr-link" '
        'href="https://protect-envi.beta.gouv.fr/demarrer-constatation">Démarrer</a> et '
        '<a target="_blank" rel="noopener noreferrer nofollow" class="fr-link" '
        'href="https://www.legifrance.gouv.fr/codes/article">Legifrance</a></p>'
    )
    cleaned = clean_html_links(html_input)
    assert 'href="/demarrer-constatation"' in cleaned
    assert 'href="https://protect-envi.beta.gouv.fr/demarrer-constatation"' not in cleaned
    assert (
        'class="fr-link" href="/demarrer-constatation"' in cleaned
        or 'href="/demarrer-constatation" class="fr-link"' in cleaned
    )
    assert 'target="_blank"' in cleaned
    assert 'rel="noopener noreferrer"' in cleaned
    assert "nofollow" not in cleaned


def test_clean_blocks_content():
    blocks = [
        {
            "type": "rich_text",
            "value": (
                '<p><a target="_blank" rel="noopener noreferrer nofollow" class="fr-link" '
                'href="https://protect-envi.beta.gouv.fr/test">Lien interne</a></p>'
            ),
        },
        {"type": "heading", "value": "Titre"},
    ]
    cleaned_blocks, changed = clean_blocks_content(blocks)
    assert changed is True
    assert 'href="/test"' in cleaned_blocks[0]["value"]
    assert "target=" not in cleaned_blocks[0]["value"]
    assert "rel=" not in cleaned_blocks[0]["value"]
    assert cleaned_blocks[1]["value"] == "Titre"
