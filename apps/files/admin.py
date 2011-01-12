from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from core.admin import AccountableAdmin
from apps.files.models import File

 
class FileAdmin(AccountableAdmin):
    exclude = ('user','account',)
    
admin.site.register(File, FileAdmin)
