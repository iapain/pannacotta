from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.admin import widgets

from apps.accounts.models import Account, AccountUserPermission
from core.admin import AccountableAdmin

blocked = ['admin', 'auth', 'sessions', 'contenttypes', 'sites',]

class PermissionAdmin(AccountableAdmin):
    exclude = ('account',)
    filter_horizontal = ['permissions']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.account is None:
            return super(PermissionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "user":
            kwargs["queryset"] = Account.objects.get(pk=request.account.pk).users.select_related()
            return db_field.formfield(**kwargs)
        return super(PermissionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if request.account is None:
            return super(PermissionAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == "permissions":
            kwargs['widget'] = widgets.FilteredSelectMultiple(db_field.verbose_name, (db_field.name in self.filter_vertical))
            kwargs["queryset"] = Permission.objects.filter(content_type__pk__gt=9)
            return db_field.formfield(**kwargs)
        return super(PermissionAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Account)
admin.site.register(AccountUserPermission, PermissionAdmin)
