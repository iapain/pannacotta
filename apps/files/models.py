from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from core.models import Accountable
 
class File(Accountable):
    title = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField( auto_now_add = True )
    file = models.FileField(upload_to='files')
 
    def __unicode__(self):
        return "%s | %s" % (self.title, self.file)
 
    class Meta:
        ordering=( '-timestamp', )
