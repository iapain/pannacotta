from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth.models import Permission

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.db.models import signals


class Account(models.Model):
    site = models.ForeignKey(Site, verbose_name=_("Site"), max_length=50, unique=True)
    owner = models.ForeignKey(User, related_name="account_owner", unique=True)
    users = models.ManyToManyField(User, related_name="account_user")
    
    def __unicode__(self):
        return self.site.domain
    

class AccountUserPermission(models.Model):
    account =models.ForeignKey(Account)
    user = models.ForeignKey(User)
    permissions = models.ManyToManyField(Permission, related_name="account_permission")
    
    def __unicode__(self):
        return "%s | %s" % (self.account.site, self.user.username)
