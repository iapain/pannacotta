from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from apps.accounts.models import AccountUserPermission

class AccountableAdmin(admin.ModelAdmin):
    """
    Admin class for models that subclass the abstract ``Accountable`` model.
    Handles limiting the change list to objects owned by the logged in user,
    as well as setting the owner of newly created objects to the logged in
    users belong to an account.

    """
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for ins in instances:
            ins.user = request.user
            ins.account = request.account
            ins.save()
        formset.save()

    def save_form(self, request, form, change):
        """
        Set the object's account as target account.
        """
        obj = form.save(commit=False)
        if obj.account_id is None:
            obj.account = request.account
        if obj.user_id is None:
            obj.user = request.user
        return super(AccountableAdmin, self).save_form(request, form, change)

    def queryset(self, request):
        """
        Filter the change list by current account if not a superuser.
        """
        qs = super(AccountableAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(account__id=request.account.id)
    
    def has_add_permission(self, request):
        """
        Check if login user has add permission based on account permission
        """
        if request.user.is_superuser:
            return True
        if request.user == request.account.owner:
            return True
        if not request.user in request.account.users.select_related():
            return False
        opts = self.opts
        try:
            perms = set([u"%s.%s" % (p.content_type.app_label, p.codename) for p in AccountUserPermission.objects.get(user=request.user, account=request.account).permissions.select_related()])
        except AccountUserPermission.DoesNotExist:
            return False
        return opts.app_label + '.' + opts.get_add_permission() in perms

    def has_change_permission(self, request, obj=None):
        """
        Check if login user has change permission based on account permission
        """
        if request.user.is_superuser:
            return True
        if request.user == request.account.owner:
            return True
        if not request.user in request.account.users.select_related():
            return False
        opts = self.opts
        try:
            perms = set([u"%s.%s" % (p.content_type.app_label, p.codename) for p in AccountUserPermission.objects.get(user=request.user, account=request.account).permissions.select_related()])
        except AccountUserPermission.DoesNotExist:
            return False
        return opts.app_label + '.' + opts.get_change_permission() in perms

    def has_delete_permission(self, request, obj=None):
        """
        Check if login user has delete permission based on account permission
        """
        if request.user.is_superuser:
            return True
        if request.user == request.account.owner:
            return True
        if not request.user in request.account.users.select_related():
            return False
        opts = self.opts
        try:
            perms = set([u"%s.%s" % (p.content_type.app_label, p.codename) for p in AccountUserPermission.objects.get(user=request.user, account=request.account).permissions.select_related()])
        except AccountUserPermission.DoesNotExist:
            return False
        return opts.app_label + '.' + opts.get_delete_permission() in perms
