from django.contrib.contenttypes.models import ContentType
from django.forms import fields
from django.forms.util import ValidationError
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

from djangomarkup.models import SourceText
from djangomarkup.widgets import RichTextAreaWidget

class RichTextField(fields.Field):
    widget = RichTextAreaWidget
    default_error_messages = {
        'syntax_error': _('Bad syntax in markdown formatting or template tags.'),
        'url_error':  _('Some links are invalid: %s.'),
        'link_error':  _('Some links are broken: %s.'),
    }

    def __init__(self, *args, **kwargs):
        # TODO: inform widget about selected processor (JS editor..)
        self.field_name = kwargs.pop('field_name')
        self.instance = kwargs.pop('instance')
        self.model = kwargs.pop('model')
        self.request = kwargs.pop('request')
        if self.instance:
            self.ct = ContentType.objects.get_for_model(self.instance)
        else:
            self.ct = ContentType.objects.get_for_model(self.model)
        super(RichTextField, self).__init__(*args, **kwargs)
        setattr(self.widget, '_field', self)

    def get_source(self):
        try:
            src_text = SourceText.objects.get(ct=self.ct, obj_id=self.instance.pk, field=self.field_name)
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
        if not  self.is_markup():
            return super_value
        if value in fields.EMPTY_VALUES:
            return u''
        text = smart_unicode(value)

        # TODO save value to SourceText, return rendered. post_save signal !
        from ella.newman.markup.models import SourceText, TextProcessor
        if self.instance:
            src_text, created = SourceText.objects.get_or_create(ct=self.ct, obj_id=self.instance.pk, field=self.field_name)
            src_text.content = text
            try:
                rendered = src_text.render()
            except:
                raise ValidationError(self.error_messages['syntax_error'])
            src_text.save()
        else:
            # in case of adding new model, instance is not set
            default_proc = TextProcessor.objects.get(name=config.NEWMAN_MARKUP_DEFAULT)
            src_text =  SourceText(
                ct=self.ct,
                field=self.field_name,
                content=text,
                processor=default_proc
            )
            try:
                rendered = src_text.render()
            except:
                raise ValidationError(self.error_messages['syntax_error'])
            listener_post_save.src_text = src_text
            signals.post_save.connect(listener_post_save)
        return rendered
