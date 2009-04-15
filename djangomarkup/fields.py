import logging

from django.forms import fields
from django.forms.util import ValidationError
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import signals

from django.contrib.contenttypes.models import ContentType
from djangomarkup.models import SourceText, TextProcessor
from djangomarkup.widgets import RichTextAreaWidget


log = logging.getLogger('djangomarkup')

class ListenerPostSave(object):
    def __init__(self, src_text):
        self.src_text = src_text

    def __call__(self, sender, signal, created, **kwargs):
        log.debug('Listener activated by %s, sig=%s, created=%s' % (sender, signal, created))
        log.debug('Listener kwargs=%s' % kwargs)
        src_text = self.src_text

        signals.post_save.disconnect(receiver=self, sender=src_text.content_type.model_class())
        log.debug('Signal listener disconnected')
        src_text.object_id = kwargs['instance'].pk
        src_text.save()

class RichTextField(fields.Field):
    widget = RichTextAreaWidget
    default_error_messages = {
        'syntax_error': _('Bad syntax in syntax formatting or template tags.'),
        'url_error':  _('Some links are invalid: %s.'),
        'link_error':  _('Some links are broken: %s.'),
    }

    def __init__(self, model, instance, field_name, syntax_processor_name=None, request=None, **kwargs):
        # TODO: inform widget about selected processor (JS editor..)
        self.field_name = field_name
        self.instance = instance
        self.model = model
        self.request = request
        self.processor = TextProcessor.objects.get(name=syntax_processor_name or getattr(settings, "DEFAULT_MARKUP", "markdown"))
        if self.instance:
            self.ct = ContentType.objects.get_for_model(self.instance)
        else:
            self.ct = ContentType.objects.get_for_model(self.model)

        super(RichTextField, self).__init__(**kwargs)
        self.widget._field = self

    def get_source(self):
        try:
            assert self.instance is not None, "Trying to retrieve source for unsaved object"
            src_text = SourceText.objects.get(content_type=self.ct, object_id=self.instance.pk, field=self.field_name)
        except SourceText.DoesNotExist:
            log.warning('SourceText.DoesNotExist for ct=%d obj_id=%d field=%s' % (self.ct.pk, self.instance.pk, self.field_name))
            #raise NotFoundError(u'No SourceText defined for object [%s] , field [%s] ' % ( self.instance.__unicode__(), self.field_name))
            return SourceText()
        return src_text

    def get_source_text(self):
        return self.get_source().content

    def get_rendered_text(self):
        return self.get_source().render()

    def clean(self, value):
        super_value = super(RichTextField, self).clean(value)
        if value in fields.EMPTY_VALUES:
            return u''
        text = smart_unicode(value)

        # TODO save value to SourceText, return rendered. post_save signal !
        if self.instance:
            src_text, created = SourceText.objects.get_or_create(content_type=self.ct, object_id=self.instance.pk, field=self.field_name)
            src_text.content = text
            try:
                rendered = src_text.render()
            except:
                raise ValidationError(self.error_messages['syntax_error'])
            src_text.save()
        else:
            # in case of adding new model, instance is not set
            src_text = SourceText(
                content_type=self.ct,
                field=self.field_name,
                content=text,
                processor=self.processor
            )
            try:
                rendered = src_text.render()
            except:
                raise ValidationError(self.error_messages['syntax_error'])

            listener_post_save = ListenerPostSave(src_text)
            signals.post_save.connect(receiver=listener_post_save, sender=src_text.content_type.model_class(), weak=False)
        return rendered
