from django.contrib import admin
from django.contrib.admin import widgets

from apps.blogs.models import BlogPost
from apps.tags.models import Tag

from core.admin import AccountableAdmin

class BlogPostAdmin(AccountableAdmin):
    exclude = ('user', 'account')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('publish_date', 'status')

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if request.account is None:
            return super(BlogPostAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == "tags":
            kwargs['widget'] = widgets.FilteredSelectMultiple(db_field.verbose_name, (db_field.name in self.filter_vertical))
            kwargs["queryset"] = Tag.objects.filter(account=request.account)
            return db_field.formfield(**kwargs)
        return super(BlogPostAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(BlogPost, BlogPostAdmin)

