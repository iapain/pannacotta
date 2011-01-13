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
