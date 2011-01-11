from django.contrib import admin
from models import Account, AccountUserPermission
from django.contrib.auth.models import Permission
from django.contrib.admin import widgets

blocked = ['admin', 'auth', 'sessions', 'contenttypes', 'sites',]

class PermissionAdmin(admin.ModelAdmin):
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

    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.account = request.account
        obj.save()
        
    def queryset(self, request):
        qs = super(PermissionAdmin, self).queryset(request)

        # If super-user, show all comments
        if request.user.is_superuser:
            return qs
        return qs.filter(account=request.account)
        
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user == request.account.owner:
            return True
        if not request.user in request.account.users.select_related():
            return False
        return False
        
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user == request.account.owner:
            return True
        return False
        
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user == request.account.owner:
            return True
        return False

admin.site.register(Account)
admin.site.register(AccountUserPermission, PermissionAdmin)
