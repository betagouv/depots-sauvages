from django.db import models

from backend.guillotine.models import BlockContent, OrderedContent


class BlogArticle(BlockContent, OrderedContent):
    slug = models.SlugField(max_length=255, unique=True)
    summary = models.TextField(max_length=500, blank=True)
    cover_image = models.ImageField(upload_to="blog_covers/", blank=True, null=True)

    class Meta:
        verbose_name = "Article de blog"
        verbose_name_plural = "Articles de blog"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title
