from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db import models, IntegrityError, transaction
from django.db.models.base import ModelBase
from django.template.defaultfilters import slugify as default_slugify, truncatewords_html
from django.utils.translation import ugettext, ugettext_lazy as _

class Accountable(models.Model):
    """
    Abstract model that provides ownership of an object for a user.
    """

    user = models.ForeignKey("auth.User", verbose_name=_("Author"),
        related_name="%(class)ss")
    account = models.ForeignKey("accounts.Account", verbose_name=_("Account"),
        related_name="%(class)ss")

    class Meta:
        abstract = True


class Slugable(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=200)
    slug = models.SlugField(verbose_name=_('Slug'), max_length=200)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = self.slugify(self.title)
            if django.VERSION >= (1, 2):
                from django.db import router
                using = kwargs.get("using") or router.db_for_write(
                    type(self), instance=self)
                # Make sure we write to the same db for all attempted writes,
                # with a multi-master setup, theoretically we could try to
                # write and rollback on different DBs
                kwargs["using"] = using
                trans_kwargs = {"using": using}
            else:
                trans_kwargs = {}
            i = 0
            while True:
                i += 1
                try:
                    sid = transaction.savepoint(**trans_kwargs)
                    res = super(TagBase, self).save(*args, **kwargs)
                    transaction.savepoint_commit(sid, **trans_kwargs)
                    return res
                except IntegrityError:
                    transaction.savepoint_rollback(sid, **trans_kwargs)
                    self.slug = self.slugify(self.title, i)
        else:
            return super(Slugable, self).save(*args, **kwargs)

    def slugify(self, tag, i=None):
        slug = default_slugify(tag)
        if i is not None:
            slug += "_%d" % i
        return slug

CONTENT_STATUS_DRAFT = 1
CONTENT_STATUS_PUBLISHED = 2
CONTENT_STATUS_CHOICES = (
    (CONTENT_STATUS_DRAFT, _("Draft")),
    (CONTENT_STATUS_PUBLISHED, _("Published")),
)


class Displayable(Slugable):
    """
    Abstract model that provides features of a visible page on the website
    such as publishing fields and meta data.
    """

    status = models.IntegerField(_("Status"),
        choices=CONTENT_STATUS_CHOICES, default=CONTENT_STATUS_DRAFT)
    publish_date = models.DateTimeField(_("Published from"),
        help_text=_("With published selected, won't be shown until this time"),
        blank=True, null=True)
    expiry_date = models.DateTimeField(_("Expires on"),
        help_text=_("With published selected, won't be shown after this time"),
        blank=True, null=True)
    description = models.TextField(_("description"), max_length=1000, blank=True)
    keywords = models.CharField(max_length=500, editable=False)
    short_url = models.URLField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Set default for ``publsh_date`` and ``description`` if none given.
        """
        if self.publish_date is None:
            # publish_date will be blank when a blog post is created from the
            # quick blog form in the admin dashboard.
            self.publish_date = datetime.now()
        if not self.description:
            self.description = self.description_from_content()
        super(Displayable, self).save(*args, **kwargs)

    def description_from_content(self):
        """
        Returns the first paragraph of the first content-like field.
        """
        description = ""
        # Get the value of the first HTMLField, or TextField if none found.
        for field_type in (models.TextField,):
            if not description:
                for field in self._meta.fields:
                    if isinstance(field, field_type) and \
                        field.name != "description":
                        description = getattr(self, field.name)
                        if description:
                            break
        # Fall back to the title if description couldn't be determined.
        if not description:
            description = self.title
        # Strip everything after the first paragraph or sentence.
        for end in ("</p>", "<br />", "\n", ". "):
            if end in description:
                description = description.split(end)[0] + end
                break
        else:
            description = truncatewords_html(description, 100)
        return description

