import pytest
from django.urls import reverse

from backend.blog.models import BlogArticle
from backend.faq.models import FAQItem
from backend.seo.utils import clean_text


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
    assert "<title>Qu&#x27;est-ce qu&#x27;un dépôt sauvage ? - Stop Dépôt Sauvage</title>" in content
    assert "Un dépôt sauvage est illégal et nocif pour l&#x27;environnement." in content


@pytest.mark.django_db
def test_seo_metadata_blog_article(client):
    BlogArticle.objects.create(
        title="Procédure administrative ou pénale ?",
        slug="procedure-administrative-ou-penale",
        summary="Deux voies pour agir\r\ncontre les dépôts sauvages.",
        content=[{"type": "rich_text", "value": "<p>Texte de l'article.</p>"}],
    )
    response = client.get("/blog/procedure-administrative-ou-penale")
    content = response.content.decode()
    assert "<title>Procédure administrative ou pénale ? - Stop Dépôt Sauvage</title>" in content
    assert '<meta name="description" content="Deux voies pour agir contre les dépôts sauvages." />' in content
    assert '<meta property="og:type" content="article" />' in content
    assert (
        '<link rel="canonical" href="http://testserver/blog/procedure-administrative-ou-penale" />'
        in content
    )
    assert '<meta property="og:url" content="http://testserver/blog/procedure-administrative-ou-penale" />' in content


@pytest.mark.django_db
def test_seo_metadata_blog_article_without_summary(client):
    long_text = "Un dépôt sauvage " * 20
    BlogArticle.objects.create(
        title="Sans chapô",
        slug="sans-chapo",
        content=[{"type": "rich_text", "value": f"<p>{long_text}</p>"}],
    )
    content = client.get("/blog/sans-chapo").content.decode()
    description = content.split('<meta name="description" content="')[1].split('"')[0]
    assert description.startswith("Un dépôt sauvage Un dépôt sauvage")
    assert description.endswith("...")
    assert len(description) <= 150


def test_clean_text_keeps_space_between_paragraphs():
    html = "<p>Loi AGEC de 2020.</p><p>Elle permet au maire<br>d'agir.</p><ul><li>Un</li><li>Deux</li></ul>"
    assert clean_text(html) == "Loi AGEC de 2020. Elle permet au maire d'agir. Un Deux"


@pytest.mark.django_db
@pytest.mark.parametrize("slug", ["brouillon", "inconnu"])
def test_seo_metadata_blog_article_generic_fallback(client, slug):
    BlogArticle.objects.create(title="Article en brouillon", slug="brouillon", is_published=False)
    content = client.get(f"/blog/{slug}").content.decode()
    assert "Article en brouillon" not in content
    assert "<title>Stop Dépôt Sauvage - Accompagner les collectivités" in content
    assert '<meta property="og:type" content="website" />' in content


@pytest.mark.django_db
def test_seo_metadata_blog_list(client):
    content = client.get("/blog").content.decode()
    assert "<title>Blog &amp; Retours d’expérience - Stop Dépôt Sauvage</title>" in content


@pytest.mark.django_db
def test_seo_metadata_share_tags_on_home(client):
    content = client.get("/").content.decode()
    assert '<meta property="og:type" content="website" />' in content
    assert '<link rel="canonical" href="http://testserver/" />' in content
    assert '<meta property="og:site_name" content="Stop Dépôt Sauvage" />' in content
    assert '<meta name="twitter:card" content="summary" />' in content


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
