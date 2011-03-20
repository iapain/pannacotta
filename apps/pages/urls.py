from django.conf.urls.defaults import *


# Page patterns.
urlpatterns = patterns("apps.pages.views",
   # url("^admin_page_ordering/$", "admin_page_ordering",
   #     name="admin_page_ordering"),
    url("^(?P<slug>.*)/$", "page", name="page"),
)
