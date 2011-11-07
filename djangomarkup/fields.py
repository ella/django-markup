import logging

from django.forms import fields
from django.forms.util import ValidationError
from django.utils.encoding import smart_unicode, smart_str
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import signals
from django.core import signals as core_signals

from django.contrib.contenttypes.models import ContentType
from djangomarkup.models import SourceText, TextProcessor
from djangomarkup.widgets import RichTextAreaWidget
from djangomarkup.processors import ProcessorError

RICH_FIELDS_SET = '__rich_fields_list'
SRC_TEXT_ATTR = '__src_text'

log = logging.getLogger('djangomarkup')

class UnicodeWrapper(unicode):
    def __str__(self):
        return smart_str(self)

    def __conform__(self, x):
            try:
                engine = settings.DATABASES['default']['ENGINE'].split('.')[-1]
            except (KeyError, AttributeError):
                engine = getattr(settings, 'DATABASE_ENGINE', '').split('.')[-1]

            if engine.startswith('postgresql'):
                # hack to enable psycopg2's adapting to work
                # on something that is not a unicode
                from psycopg2.extensions import adapt
                return adapt(unicode(self))
            return unicode(self)

def post_save_listener(sender, instance, src_text_attr=SRC_TEXT_ATTR, **kwargs):
    src_texts = []
    for f in getattr(sender, RICH_FIELDS_SET, []):
        rendered = getattr(instance, f)
        if not isinstance(rendered, UnicodeWrapper) or not hasattr(rendered, src_text_attr):
            continue

        src_text = getattr(rendered, src_text_attr)
        src_text.object_id = instance.pk
        src_text.save()
        src_texts.append(src_text)
    return src_texts

class RichTextField(fields.Field):
    # default post save listenere. Override this to provide custom logic in wrapper
    post_save_listener = staticmethod(post_save_listener)
    src_text_attr = SRC_TEXT_ATTR

    # default widget
    widget = RichTextAreaWidget

    # default messages
    default_error_messages = {
        'syntax_error': _('Bad syntax in syntax formatting or template tags.'),
        'url_error':  _('Some links are invalid: %s.'),
        'link_error':  _('Some links are broken: %s.'),
    }

    __inst_counter = 0

    def __init__(self, model, field_name, instance=None, syntax_processor_name=None, **kwargs):
        # TODO: inform widget about selected processor (JS editor..)

        if 'request' in kwargs:
            kwargs.pop('request')

        self.field_name = field_name
        self.instance = instance
        self.model = model
        self.processor = TextProcessor.objects.get(name=syntax_processor_name or getattr(settings, "DEFAULT_MARKUP", "markdown"))
        self.ct = ContentType.objects.get_for_model(model)

        super(RichTextField, self).__init__(**kwargs)
        self.widget._field = self

    def get_instance_id(self, instance):
        " Returns instance pk even if multiple instances were passed to RichTextField. "
        if type(instance) in [list, tuple]:
            core_signals.request_finished.connect(receiver=RichTextField.reset_instance_counter_listener)
            if RichTextField.__inst_counter >= len(instance):
                return None
            else:
                obj_id = self.instance[ RichTextField.__inst_counter ].pk
            RichTextField.__inst_counter += 1
        else:
            obj_id = instance.pk
        return obj_id

    @staticmethod
    def reset_instance_counter_listener(*args, **kwargs):
        core_signals.request_finished.disconnect(receiver=RichTextField.reset_instance_counter_listener)
        RichTextField.__inst_counter = 0

    def get_source(self):
        try:
            if self.instance is None:
                raise ValueError("Trying to retrieve source, but no object is available")
            obj_id = self.get_instance_id(self.instance)
            if not obj_id:
                return SourceText(processor=self.processor)
            src_text = SourceText.objects.get(content_type=self.ct, object_id=obj_id, field=self.field_name)
        except SourceText.DoesNotExist:
            log.warning('SourceText.DoesNotExist for ct=%s obj_id=%s field=%s' % (self.ct.pk, obj_id, self.field_name))
            #raise NotFoundError(u'No SourceText defined for object [%s] , field [%s] ' % ( self.instance.__unicode__(), self.field_name))
            src_text = SourceText(processor=self.processor)

        return src_text

    def get_source_text(self):
        return self.get_source().content

    def get_rendered_text(self):
        return self.get_source().render()

    def validate_rendered(self, rendered):
        """
        Hook for addition validations subclasses might want to impose (HTML sanitization for example).
        """
        pass

    def clean(self, value):
        """
        When cleaning field, store original value to SourceText model and return rendered field.
        @raise ValidationError when something went wrong with transformation.
        """
        super_value = super(RichTextField, self).clean(value)

        if super_value in fields.EMPTY_VALUES:
            if self.instance:
                obj_id = self.get_instance_id(self.instance)
                if not obj_id:
                    SourceText.objects.filter(content_type=self.ct, object_id=obj_id, field=self.field_name, processor=self.processor).delete()
                else:
                    SourceText.objects.filter(content_type=self.ct, object_id=obj_id, field=self.field_name).delete()
            self.validate_rendered('')
            return ''

        text = smart_unicode(value)
        if self.instance:
            obj_id = self.get_instance_id(self.instance)
            try:
                if not obj_id:
                    src_text = SourceText(content_type=self.ct, object_id=obj_id, field=self.field_name, processor=self.processor)
                else:
                    src_text = SourceText.objects.get(content_type=self.ct, object_id=obj_id, field=self.field_name)
                assert src_text.processor == self.processor
            except SourceText.DoesNotExist:
                src_text = SourceText(content_type=self.ct, object_id=obj_id, field=self.field_name, processor=self.processor)
            src_text.content = text
            try:
                rendered = src_text.render()
            except ProcessorError, e:
                raise ValidationError(self.error_messages['syntax_error'])
        else:
            # in case of adding new model, instance is not set
            self.instance = src_text = SourceText(
                content_type=self.ct,
                field=self.field_name,
                content=text,
                processor=self.processor
            )
            try:
                rendered = src_text.render()
            except Exception, err:
                raise ValidationError(self.error_messages['syntax_error'])

        self.validate_rendered(rendered)

        if not hasattr(self.model, RICH_FIELDS_SET):
            setattr(self.model, RICH_FIELDS_SET, set())
        getattr(self.model, RICH_FIELDS_SET).add(self.field_name)

        # register the listener that saves the SourceText
        #listener = self.post_save_listener(src_text)
        signals.post_save.connect(receiver=self.post_save_listener, sender=self.model)

        # wrap the text so that we can store the src_text on it
        rendered = UnicodeWrapper(rendered)
        setattr(rendered, self.src_text_attr, src_text)

        return rendered
