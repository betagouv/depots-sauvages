import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from backend.blog.models import BlogArticle

User = get_user_model()


@pytest.mark.django_db
class TestBlogIntegration:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user", password="password")
        self.admin = User.objects.create_superuser(username="admin", password="password")
        self.article1 = BlogArticle.objects.create(
            title="Premier article",
            summary="Résumé du premier article",
            content=[{"type": "rich_text", "value": "<p>Contenu du premier article</p>"}],
            is_published=True,
            order=1,
        )
        self.article2 = BlogArticle.objects.create(
            title="Deuxième article",
            summary="Résumé du deuxième article",
            content=[{"type": "rich_text", "value": "<p>Contenu du deuxième article</p>"}],
            is_published=False,
            order=2,
        )

    def test_anonymous_list_only_published(self):
        response = self.client.get("/api/blog-articles/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Premier article"

    def test_admin_list_all(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/blog-articles/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2

    def test_get_article_by_slug(self):
        response = self.client.get(f"/api/blog-articles/{self.article1.slug}/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Premier article"
        assert data["summary"] == "Résumé du premier article"

    def test_anonymous_cannot_mutate(self):
        response = self.client.post(
            "/api/blog-articles/",
            {"title": "Nouvel article", "summary": "Court résumé"},
            format="json",
        )
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_admin_can_create_and_reorder(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/blog-articles/",
            {"title": "Nouvel article", "summary": "Court résumé", "is_published": True},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        new_slug = response.json()["slug"]
        move_resp = self.client.post(f"/api/blog-articles/{new_slug}/move-up/")
        assert move_resp.status_code == status.HTTP_200_OK
