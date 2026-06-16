import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from backend.faq.models import FAQItem

User = get_user_model()


@pytest.mark.django_db
class TestGuillotineViews:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(username="admin", password="password")
        self.user = User.objects.create_user(username="user", password="password")

    def test_reorder_mixin_move_up_and_down(self):
        """Verifies move-up and move-down actions swap order correctly."""
        self.client.force_authenticate(user=self.admin)

        # Create items
        item1 = FAQItem.objects.create(title="Item 1", order=1)
        item2 = FAQItem.objects.create(title="Item 2", order=2)
        item3 = FAQItem.objects.create(title="Item 3", order=3)

        # Move item3 up (swapping item2 and item3)
        response = self.client.post(f"/api/faq-items/{item3.id}/move-up/")
        assert response.status_code == status.HTTP_200_OK

        item2.refresh_from_db()
        item3.refresh_from_db()
        assert item2.order == 3
        assert item3.order == 2

        # Move item3 down (swapping back)
        response = self.client.post(f"/api/faq-items/{item3.id}/move-down/")
        assert response.status_code == status.HTTP_200_OK

        item2.refresh_from_db()
        item3.refresh_from_db()
        assert item2.order == 2
        assert item3.order == 3

    def test_reorder_mixin_permissions(self):
        """Verifies that non-admin users cannot trigger reordering."""
        self.client.force_authenticate(user=self.user)
        item1 = FAQItem.objects.create(title="Item 1", order=1)

        response = self.client.post(f"/api/faq-items/{item1.id}/move-up/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
