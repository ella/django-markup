from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # serve static files
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT, 'show_indexes': True }),
    (r'^admin/(.*)', admin.site.root),

)

