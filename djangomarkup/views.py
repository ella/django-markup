import logging

from django import template
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils.translation import ugettext

from djangomarkup.models import TextProcessor

log = logging.getLogger('djangomarkup')

def transform(request, syntax_processor_name=None, var_name="text"):
    """
    Returns rendered HTML for source text
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed("Only POST allowed")
    
    source = request.POST.get(var_name)
    if not source:
        return HttpResponse('')

    processor = TextProcessor.objects.get(name=syntax_processor_name or getattr(settings, "DEFAULT_MARKUP", "markdown"))
    output = processor.convert(source)

    try:
        t = template.Template(output, name='markup_preview')
        output = t.render(template.Context({'MEDIA_URL' : settings.MEDIA_URL}))
    except template.TemplateSyntaxError, e:
        log.error('Error in preview rendering: %s' % e)
        output = '<h3 style="color:red">%s</h3><p>%s</p>' % (ugettext('You have an errors in source text!'), e)

    return HttpResponse(output)

# backward compatibility
preview = transform
