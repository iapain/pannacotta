from django.contrib import admin

from apps.tags.models import Tag, TaggedItem
from core.admin import AccountableAdmin

class TaggedItemInline(admin.StackedInline):
    exclude = ('user', 'account')
    model = TaggedItem

class TagAdmin(AccountableAdmin):
    exclude = ('user', 'account')
    inlines = [
        TaggedItemInline
    ]


admin.site.register(Tag, TagAdmin)
