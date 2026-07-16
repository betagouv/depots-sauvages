from django.db import models

from backend.guillotine.models import BlockContent


class SiteContent(BlockContent):
    """
    Model representing editable content sections across the site.
    Identified by a unique slug (e.g., 'webinaire-notice', 'home-stats').
    """

    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Contenu de site"
        verbose_name_plural = "Contenus de site"

    def __str__(self):
        return f"{self.title} ({self.slug})"
