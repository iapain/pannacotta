from django.conf.urls.defaults import *
 
urlpatterns = patterns('apps.pages.views',
    (r'^(?P<url>.*)$', 'flatpage'),
)