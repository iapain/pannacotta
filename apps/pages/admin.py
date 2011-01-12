from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from core.admin import AccountableAdmin
from models import ContentPage
 
class ContentPageAdmin(AccountableAdmin):
    exclude = ('user', 'account')

    class Media:
        js = ('/static/js/jquery.js',
            '/static/js/wymeditor/jquery.wymeditor.js',
            '/static/js/admin_textarea.js',
            '/static/js/wymeditor/plugins/jquery.wymeditor.files.js',)

    
 
admin.site.register(ContentPage, ContentPageAdmin)
