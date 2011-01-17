from django.db import models
from django.template.defaultfilters import truncatewords_html
from django.utils.translation import ugettext, ugettext_lazy as _

from core.models import Displayable, Accountable

class BlogPost(Accountable, Displayable):
    """
    A blog post.
    """
    content = models.TextField(_("content"))
    tags = models.ManyToManyField("tags.Tag", blank=True, null=True)
    #objects = BlogPostManager()

    class Meta:
        verbose_name = _("Blog post")
        verbose_name_plural = _("Blog posts")
        ordering = ("-publish_date",)

    @models.permalink
    def get_absolute_url(self):
        return ("blog_post_detail", (), {"slug": self.slug})
