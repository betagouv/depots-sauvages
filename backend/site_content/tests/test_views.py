import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from backend.site_content.models import SiteContent
from backend.unit_tests.factories import UserFactory

User = get_user_model()


@pytest.mark.django_db(databases=["default"])
def test_site_content_api_anonymous():
    client = APIClient()
    # Create a published item
    SiteContent.objects.create(
        title="Notice 1",
        slug="webinaire-notice",
        content=[{"type": "rich_text", "value": "Hello world"}],
        is_published=True,
    )
    # Create an unpublished item
    SiteContent.objects.create(
        title="Notice 2",
        slug="draft-notice",
        content=[{"type": "rich_text", "value": "Secret draft"}],
        is_published=False,
    )
    url_published = "/api/site-content/webinaire-notice/"
    response = client.get(url_published)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Notice 1"
    url_draft = "/api/site-content/draft-notice/"
    response = client.get(url_draft)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # Test POST is forbidden
    response_post = client.post("/api/site-content/", {"title": "New", "slug": "new-slug"})
    assert response_post.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db(databases=["default"])
def test_site_content_api_staff():
    client = APIClient()
    user = UserFactory(is_staff=True)
    client.force_login(user)
    # Create an unpublished item
    SiteContent.objects.create(
        title="Draft Notice",
        slug="draft-notice",
        content=[{"type": "rich_text", "value": "Secret draft"}],
        is_published=False,
    )
    # Staff can retrieve draft
    url_draft = "/api/site-content/draft-notice/"
    response = client.get(url_draft)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["is_published"] is False
    # Staff can create
    response_post = client.post(
        "/api/site-content/",
        {
            "title": "Created Banner",
            "slug": "created-banner",
            "content": [{"type": "rich_text", "value": "Dynamic banner"}],
            "is_published": True,
        },
        format="json",
    )
    assert response_post.status_code == status.HTTP_201_CREATED
    assert SiteContent.objects.filter(slug="created-banner").exists()
    # Staff can patch
    url_created = "/api/site-content/created-banner/"
    response_patch = client.patch(url_created, {"title": "Updated Banner"}, format="json")
    assert response_patch.status_code == status.HTTP_200_OK
    assert SiteContent.objects.get(slug="created-banner").title == "Updated Banner"
