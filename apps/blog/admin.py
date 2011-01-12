from django.contrib import admin
from appadmin.admin_perm import PermAdmin
from models import Category, Post
from apps.accounts.models import UserPermission


class CategoryAdmin(PermAdmin):
    exclude = ('user', 'account',)
    prepopulated_fields = {"slug": ("title",)}
   

class BlogAdmin(PermAdmin):
    prepopulated_fields = {"slug": ("title",)}

    
    fieldsets = (
        (None, {
            'fields': ('title', 'body', 'status', 'tags')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('slug', 'allow_comments', 'publish', 'categories')
        }),
    )

admin.site.register(Post, BlogAdmin)
admin.site.register(Category, CategoryAdmin)