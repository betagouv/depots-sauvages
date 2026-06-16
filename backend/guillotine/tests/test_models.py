import pytest

from backend.faq.models import FAQItem


@pytest.mark.django_db
class TestGuillotineModels:
    def test_block_content_slug_generation(self):
        """Verifies that block content automatically generates slug on save."""
        item = FAQItem.objects.create(title="Nouvelle Question Sans Slug")
        assert item.slug == "nouvelle-question-sans-slug"

        # Check slug remains optional/modifiable
        item.slug = "custom-slug-123"
        item.save()
        item.refresh_from_db()
        assert item.slug == "custom-slug-123"

    def test_nested_content_top_level(self):
        """Verifies is_top_level property and top_level queryset filtering."""
        parent = FAQItem.objects.create(title="Parent", parent=None)
        child = FAQItem.objects.create(title="Child", parent=parent)

        assert parent.is_top_level is True
        assert child.is_top_level is False

        top_items = list(FAQItem.objects.top_level())
        assert parent in top_items
        assert child not in top_items

    def test_queryset_published_filter(self):
        """Verifies published() queryset filtering method."""
        item_published = FAQItem.objects.create(title="Pub", is_published=True)
        item_draft = FAQItem.objects.create(title="Draft", is_published=False)

        all_items = list(FAQItem.objects.all())
        assert item_published in all_items
        assert item_draft in all_items

        published_only = list(FAQItem.objects.published())
        assert item_published in published_only
        assert item_draft not in published_only

    def test_nested_content_automatic_order_assignment(self):
        """Verifies that NestedContent automatically assigns next order within its parent group on creation if set to 0/None."""
        parent = FAQItem.objects.create(title="Parent", parent=None, order=1)

        child1 = FAQItem.objects.create(title="Child 1", parent=parent)
        assert child1.order == 1

        child2 = FAQItem.objects.create(title="Child 2", parent=parent)
        assert child2.order == 2

        top_level_count = FAQItem.objects.filter(parent=None).count()
        new_top_level = FAQItem.objects.create(title="New Top Level", parent=None)
        assert new_top_level.order == top_level_count + 1
