import pytest
from django.urls import reverse

from backend.faq.models import FAQItem


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
    assert "Foire Aux Questions - Protect&#x27;Envi" in content

    # Fetch dynamic faq item page to check dynamic seo
    response = client.get("/faq/qu-est-ce-qu-un-depot-sauvage")
    assert response.status_code == 200
    content = response.content.decode()
    assert "Qu&#x27;est-ce qu&#x27;un dépôt sauvage ? FAQ - Protect&#x27;Envi" in content
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
