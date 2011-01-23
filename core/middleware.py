try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
 
_thread_locals = local()

def get_current_request():
    return getattr(_thread_locals, 'request', None)

from django.conf import settings
from apps.accounts.models import Account

class SubdomainMiddleware:
    """ Make the subdomain publicly available to classes """
    
    def process_request(self, request):
        domain = request.get_host().split(':')[0] # no port
        try:
            request.account = Account.objects.get(site__domain__iexact=domain)
        except Account.DoesNotExist:
            request.account = None
        request.domain = domain
        _thread_locals.request = request
