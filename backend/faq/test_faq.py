import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from backend.faq.models import FAQItem

User = get_user_model()


@pytest.mark.django_db
class TestFAQIntegration:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user", password="password")
        self.admin = User.objects.create_superuser(username="admin", password="password")
        # Set up a category and child questions
        self.category = FAQItem.objects.create(title="⚖️ Cadre général", parent=None, order=1)
        self.question = FAQItem.objects.create(
            title="Qu'est-ce qu'un dépôt sauvage ?", parent=self.category, order=1
        )
        self.question.content = [{"type": "rich_text", "value": "<p>Un dépôt sauvage est...</p>"}]
        self.question.save()

    def test_faq_list_endpoint(self):
        """Verifies that the FAQ API list endpoint is accessible and returns the items."""
        response = self.client.get("/api/faq-items/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "top_level" in data
        assert "orphans" in data
        assert len(data["top_level"]) == 1
        assert data["top_level"][0]["title"] == "⚖️ Cadre général"
        assert len(data["top_level"][0]["children"]) == 1
        assert data["top_level"][0]["children"][0]["title"] == "Qu'est-ce qu'un dépôt sauvage ?"
