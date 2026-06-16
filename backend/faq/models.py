from backend.guillotine.models import BlockContent, NestedContent


class FAQItem(BlockContent, NestedContent):
    """
    FAQ item.
    """

    class Meta:
        verbose_name = "Question de FAQ"
        verbose_name_plural = "Questions de FAQ"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title
