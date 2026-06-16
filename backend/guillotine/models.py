from django.db import models, transaction
from django.utils.text import slugify


class ContentQuerySet(models.QuerySet):
    """Custom QuerySet to handle content filtering."""

    def published(self):
        if hasattr(self.model, "is_published"):
            return self.filter(is_published=True)
        return self

    def top_level(self):
        if hasattr(self.model, "parent"):
            return self.filter(parent__isnull=True)
        return self


class ContentManager(models.Manager.from_queryset(ContentQuerySet)):
    """Custom manager exposing ContentQuerySet custom filters."""

    pass


class BlockContent(models.Model):
    """
    Abstract mixin for block-based content.
    Manages the page envelope (title, optional slug, publication status, content blocks).
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    content = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    objects = ContentManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class NestedContent(models.Model):
    """
    Abstract mixin for nested content.
    Manages parent/child hierarchy and display order.
    """

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    order = models.PositiveIntegerField(default=0)

    objects = ContentManager()

    class Meta:
        abstract = True
        ordering = ["order", "id"]

    @property
    def is_top_level(self):
        return self.parent_id is None

    def move_up(self):
        """
        Swap order with the sibling immediately above.
        """
        sibling = (
            self.__class__.objects.filter(parent=self.parent, order__lt=self.order)
            .order_by("-order")
            .first()
        )
        if sibling:
            with transaction.atomic():
                self.order, sibling.order = sibling.order, self.order
                self.save(update_fields=["order"])
                sibling.save(update_fields=["order"])
            return True
        return False

    def move_down(self):
        """
        Swap order with the sibling immediately below.
        """
        sibling = (
            self.__class__.objects.filter(parent=self.parent, order__gt=self.order)
            .order_by("order")
            .first()
        )
        if sibling:
            with transaction.atomic():
                self.order, sibling.order = sibling.order, self.order
                self.save(update_fields=["order"])
                sibling.save(update_fields=["order"])
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.pk and (self.order == 0 or self.order is None):
            siblings = self.__class__.objects.filter(parent=self.parent)
            if siblings.exists():
                max_order = siblings.aggregate(models.Max("order"))["order__max"]
                self.order = (max_order or 0) + 1
            else:
                self.order = 1
        super().save(*args, **kwargs)
