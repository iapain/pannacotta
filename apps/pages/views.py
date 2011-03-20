from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import loader, RequestContext
from django.utils.http import urlquote
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe
from django.db.models import get_model

from apps.pages.models import *

def page(request, slug, template='pages/page.html'):
    page = get_object_or_404(Page, slug=slug, account=request.account)
    if page.login_required and not request.user.is_authenticated():
        return redirect("%s?%s=%s" % (settings.LOGIN_URL, REDIRECT_FIELD_NAME,
            urlquote(request.get_full_path())))

    page = get_model('pages', page.content_model).objects.get(pk=page.pk)

    if hasattr(page, 'template') and page.template:
        t = loader.select_template((page.template.name,))
    else:
        t = loader.get_template(template)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    page.title = mark_safe(page.title)
    page.content = mark_safe(page.content)
    context = {"page": page}
    c = RequestContext(request, context)
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, Page, page.id)
    return response

