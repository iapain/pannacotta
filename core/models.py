from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.base import ModelBase
from django.template.defaultfilters import slugify, truncatewords_html
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


