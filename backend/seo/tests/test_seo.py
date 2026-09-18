import json
import re

import pytest
from django.urls import reverse

from backend.blog.models import BlogArticle
from backend.faq.models import FAQItem


def create_article(**overrides):
    defaults = {
        "title": "Amende administrative pour dépôt sauvage : comment ça marche ?",
        "slug": "amende-administrative-pour-depot-sauvage-comment-ca-marche",
        "summary": "Comment fixer le montant d'une amende administrative après un dépôt sauvage.",
        "content": [{"type": "rich_text", "value": "<p>Le maire peut sanctionner.</p>"}],
    }
    defaults.update(overrides)
    return BlogArticle.objects.create(**defaults)


@pytest.mark.django_db
@pytest.mark.parametrize("env", ["staging", "dev", "local", "development"])
def test_middleware_non_prod_headers(client, settings, env):
    settings.ENV_NAME = env
    response = client.get(reverse("index"))
    assert response["X-Robots-Tag"] == "noindex, nofollow"


@pytest.mark.django_db
def test_middleware_prod_headers(client, settings):
    settings.ENV_NAME = "prod"
    response = client.get(reverse("index"))
    assert "X-Robots-Tag" not in response


@pytest.mark.django_db
def test_seo_metadata_dynamic_faq(client):
    FAQItem.objects.create(
        title="Qu'est-ce qu'un dépôt sauvage ?",
        slug="qu-est-ce-qu-un-depot-sauvage",
        content=[
            {
                "type": "rich_text",
                "value": "<p>Un dépôt sauvage est <strong>illégal</strong> et nocif pour l'environnement.</p>",
            }
        ],
    )
    # Fetch base faq page to check static seo
    response = client.get("/faq")
    assert response.status_code == 200
    content = response.content.decode()
    assert "Foire Aux Questions - Stop Dépôt Sauvage" in content

    # Fetch dynamic faq item page to check dynamic seo
    response = client.get("/faq/qu-est-ce-qu-un-depot-sauvage")
    assert response.status_code == 200
    content = response.content.decode()
    assert "Qu&#x27;est-ce qu&#x27;un dépôt sauvage ? FAQ - Stop Dépôt Sauvage" in content
    assert "Un dépôt sauvage est illégal et nocif pour l&#x27;environnement." in content


@pytest.mark.django_db
@pytest.mark.parametrize("env", ["staging", "dev", "local", "development"])
def test_robots_txt_non_prod(client, settings, env):
    settings.ENV_NAME = env
    response = client.get(reverse("robots_txt"))
    assert response.status_code == 200
    assert "text/plain" in response["Content-Type"]
    content = response.content.decode()
    assert "Allow: /" in content
    assert "Disallow: /" not in content


@pytest.mark.django_db
def test_robots_txt_prod(client, settings):
    settings.ENV_NAME = "prod"
    settings.ADMIN_URL_NAME = "my-custom-admin-portal"
    response = client.get(reverse("robots_txt"))
    assert response.status_code == 200
    assert "text/plain" in response["Content-Type"]
    content = response.content.decode()
    assert "Disallow: /my-custom-admin-portal/" in content
    assert "Allow: /" in content


@pytest.mark.django_db
@pytest.mark.parametrize("env", ["staging", "dev", "local", "development"])
def test_seo_robots_meta_non_prod(client, settings, env):
    settings.ENV_NAME = env
    response = client.get(reverse("index"))
    assert response.status_code == 200
    content = response.content.decode()
    assert '<meta name="robots" content="noindex, nofollow" />' in content


@pytest.mark.django_db
def test_seo_robots_meta_prod(client, settings):
    settings.ENV_NAME = "prod"
    response = client.get(reverse("index"))
    assert response.status_code == 200
    content = response.content.decode()
    assert '<meta name="robots" content="index, follow" />' in content


@pytest.mark.django_db
def test_seo_metadata_blog_article(client):
    create_article()
    response = client.get("/blog/amende-administrative-pour-depot-sauvage-comment-ca-marche")
    assert response.status_code == 200
    content = response.content.decode()
    # Titre de 62 caractères : le suffixe du site ne tient pas, on garde le titre seul.
    assert (
        "<title>Amende administrative pour dépôt sauvage : comment ça marche ?</title>" in content
    )
    assert "Comment fixer le montant d&#x27;une amende administrative" in content
    assert '<meta property="og:type" content="article" />' in content


@pytest.mark.django_db
def test_seo_metadata_blog_short_title_gets_site_suffix(client):
    create_article(title="Dépôt sauvage : agir vite", slug="depot-sauvage-agir-vite")
    response = client.get("/blog/depot-sauvage-agir-vite")
    content = response.content.decode()
    assert "<title>Dépôt sauvage : agir vite - Stop Dépôt Sauvage</title>" in content


@pytest.mark.django_db
def test_seo_metadata_blog_long_summary_is_truncated(client):
    create_article(
        slug="chapo-trop-long",
        summary="Procédure administrative ou pénale : que choisir ?\r\nFace à un dépôt sauvage, "
        "faut-il engager une procédure administrative ou pénale ?\r\nDifférences, avantages et "
        "cas d'usage pour les maires et agents des collectivités territoriales.",
    )
    response = client.get("/blog/chapo-trop-long")
    content = response.content.decode()
    description = re.search(r'<meta name="description" content="(.*?)" />', content).group(1)
    assert len(description) <= 155
    assert description.endswith("…")
    # Les retours à la ligne du champ de saisie ne doivent pas ressortir.
    assert "\r" not in description and "\n" not in description


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path",
    ["/blog/brouillon-non-publie", "/blog/slug-inexistant"],
)
def test_seo_metadata_blog_draft_and_unknown_fall_back_to_default(client, path):
    create_article(slug="brouillon-non-publie", is_published=False)
    response = client.get(path)
    assert response.status_code == 200
    content = response.content.decode()
    assert "Stop Dépôt Sauvage - Accompagner les collectivités" in content
    assert '<meta property="og:type" content="website" />' in content


@pytest.mark.django_db
def test_seo_metadata_blog_list_page(client):
    response = client.get("/blog")
    content = response.content.decode()
    assert "Blog &amp; Retours d&#x27;expérience - Stop Dépôt Sauvage" in content


@pytest.mark.django_db
def test_canonical_and_social_tags(client, settings):
    settings.SITE_BASE_URL = "https://stopdepotsauvage.beta.gouv.fr"
    response = client.get("/comment-agir")
    content = response.content.decode()
    canonical = "https://stopdepotsauvage.beta.gouv.fr/comment-agir"
    assert f'<link rel="canonical" href="{canonical}" />' in content
    assert f'<meta property="og:url" content="{canonical}" />' in content
    assert '<meta property="og:site_name" content="Stop Dépôt Sauvage" />' in content
    assert '<meta property="og:locale" content="fr_FR" />' in content
    assert '<meta name="twitter:card" content="summary_large_image" />' in content
    assert (
        '<meta property="og:image" content="https://stopdepotsauvage.beta.gouv.fr'
        '/static/depot-de-dechet-sauvage-image-accueil.webp" />' in content
    )


@pytest.mark.django_db
def test_blog_article_exposes_structured_data(client, settings):
    settings.SITE_BASE_URL = "https://stopdepotsauvage.beta.gouv.fr"
    article = create_article()
    response = client.get(f"/blog/{article.slug}")
    content = response.content.decode()
    raw = re.search(
        r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL
    ).group(1)
    data = json.loads(raw.replace("\\u003C", "<"))
    assert data["@type"] == "BlogPosting"
    assert data["headline"] == article.title
    assert data["url"] == f"https://stopdepotsauvage.beta.gouv.fr/blog/{article.slug}"
    assert data["datePublished"]
    assert data["publisher"]["name"] == "Stop Dépôt Sauvage"


@pytest.mark.django_db
def test_no_structured_data_outside_articles(client):
    response = client.get("/faq")
    assert "application/ld+json" not in response.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path",
    ["/mes-procedures", "/suivi-procedure/12", "/tableau-de-bord", "/constatation-fin/3"],
)
def test_private_pages_are_not_indexable_in_prod(client, settings, path):
    settings.ENV_NAME = "prod"
    response = client.get(path)
    content = response.content.decode()
    assert '<meta name="robots" content="noindex, nofollow" />' in content


@pytest.mark.django_db
def test_public_pages_stay_indexable_in_prod(client, settings):
    settings.ENV_NAME = "prod"
    response = client.get("/blog")
    assert '<meta name="robots" content="index, follow" />' in response.content.decode()


@pytest.mark.django_db
def test_sitemap_lists_published_content_only(client, settings):
    settings.SITE_BASE_URL = "https://stopdepotsauvage.beta.gouv.fr"
    create_article()
    create_article(title="Brouillon", slug="brouillon", is_published=False)
    FAQItem.objects.create(title="Une question ?", slug="une-question")

    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    content = response.content.decode()

    assert (
        "https://stopdepotsauvage.beta.gouv.fr/blog/"
        "amende-administrative-pour-depot-sauvage-comment-ca-marche" in content
    )
    assert "https://stopdepotsauvage.beta.gouv.fr/faq/une-question" in content
    assert "https://stopdepotsauvage.beta.gouv.fr/comment-agir" in content
    assert "/blog/brouillon" not in content
    # Les pages privées n'ont rien à faire dans un sitemap.
    assert "/mes-procedures" not in content
    assert "/tableau-de-bord" not in content


@pytest.mark.django_db
def test_robots_txt_announces_sitemap(client, settings):
    settings.ENV_NAME = "prod"
    settings.SITE_BASE_URL = "https://stopdepotsauvage.beta.gouv.fr"
    response = client.get(reverse("robots_txt"))
    content = response.content.decode()
    assert "Sitemap: https://stopdepotsauvage.beta.gouv.fr/sitemap.xml" in content
