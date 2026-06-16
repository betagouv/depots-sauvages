import pytest

from backend.faq.models import FAQItem


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
