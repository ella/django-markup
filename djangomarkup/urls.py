from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('djangomarkup.views',
    url(r'^transform/(?P<syntax_processor_name>[a-z\-]+)?/$', 'transform', name="markup-transform"),
)

