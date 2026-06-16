import pytest
from django.contrib.auth import get_user_model

from backend.faq.models import FAQItem
from backend.faq.serializers import FAQItemSerializer

User = get_user_model()


@pytest.mark.django_db
class TestGuillotineSerializers:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.user = User.objects.create_user(username="user", password="password")
        self.staff_user = User.objects.create_user(
            username="staff", password="password", is_staff=True
        )

        self.parent = FAQItem.objects.create(title="Parent", parent=None)
        self.child_published = FAQItem.objects.create(
            title="Child Pub", parent=self.parent, is_published=True
        )
        self.child_published.content = [{"type": "rich_text", "value": "<p>Content</p>"}]
        self.child_published.save()

        self.child_draft = FAQItem.objects.create(
            title="Child Draft", parent=self.parent, is_published=False
        )
        self.child_draft.content = [{"type": "rich_text", "value": "<p>Draft</p>"}]
        self.child_draft.save()

    def test_block_content_mixin_serialization(self):
        """Verifies raw JSON block serialization and deserialization."""
        # Test serialization (returns raw JSON list of blocks)
        serializer = FAQItemSerializer(self.child_published)
        assert serializer.data["content"] == [{"type": "rich_text", "value": "<p>Content</p>"}]

        # Test deserialization (accepts raw JSON list of blocks)
        data = {"title": "New", "content": [{"type": "rich_text", "value": "<p>Raw HTML</p>"}]}
        serializer = FAQItemSerializer(data=data)
        assert serializer.is_valid() is True
        assert serializer.validated_data["content"] == [
            {"type": "rich_text", "value": "<p>Raw HTML</p>"}
        ]

    def test_nested_content_mixin_children_recursive_user(self):
        """Verifies that normal users only see published children."""
        serializer = FAQItemSerializer(
            self.parent, context={"request": type("Request", (), {"user": self.user})}
        )
        children = serializer.data["children"]
        assert len(children) == 1
        assert children[0]["title"] == "Child Pub"

    def test_nested_content_mixin_children_recursive_staff(self):
        """Verifies that staff users see all children (published and draft)."""
        serializer = FAQItemSerializer(
            self.parent, context={"request": type("Request", (), {"user": self.staff_user})}
        )
        children = serializer.data["children"]
        assert len(children) == 2
        titles = [child["title"] for child in children]
        assert "Child Pub" in titles
        assert "Child Draft" in titles
