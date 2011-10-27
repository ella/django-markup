from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.importlib import import_module

from djangomarkup.processors import ProcessorConfigurationError, ProcessorError

#class RichTextField(models.TextField):
#    def __init__(self, syntax, *args, **kwargs):
#        self.syntax = syntax
#        super(RichTextField, self).__init__(*args, **kwargs)
#
#    def formfield(self, **kwargs):
#        from djangomarkup.fields import RichTextField as RichTextFormField
#        kwargs.update({
#            'syntax' : self.syntax,
#            'field_name' : self.name,
#
#        })
#        return RichTextFormField(**kwargs)

class TextProcessor(models.Model):
    """
    Text processors are used to convert user-inputted source text in given processor format
    (i.e. Markdown, Czechtile, ...) and convert them into target format
    (now XHTML is assumed)
    """
    function = models.CharField(max_length=96, unique=True)
    name = models.CharField(max_length=96, blank=True)
    processor_options = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    def get_function(self):
        """
        Return function object for my function.
        raise ProcessorConfigurationError when function could not be resolved.
        """
        if not hasattr(self, '_function'):
            try:
                modname, funcname = self.function.rsplit('.', 1)
                mod = import_module(modname)
                self._function = getattr(mod, funcname)
            except (ImportError, AttributeError, ValueError), err:
                raise ProcessorConfigurationError(err)

        return self._function

    def convert(self, src_txt):
        function = self.get_function()
        try:
            return unicode(function(src_txt))
        except Exception, err:
            raise ProcessorError(err)

    class Meta:
        verbose_name = (_('Text processor'))
        verbose_name_plural = (_('Text processors'))


class SourceTextManager(models.Manager):
    def delete_for_object(self, instance):
        try:
            pk = int(instance.pk)
        except ValueError:
            return

        self.filter(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=pk,
        ).delete()

    def extract_from_instance(self, instance, processor, fields, content_type=None, force_save=False, force_create=False):
        if not content_type:
            content_type = ContentType.objects.get_for_model(instance)

        dirty = False
        for f in fields:
            val = getattr(instance, f)
            if not val:
                continue

            if force_create:
                created = True
                st = self.create(
                            content_type=content_type,
                            object_id=instance.pk,
                            field=f,
                            processor=processor,
                            content=val,
                    )
            else:
                st, created = self.get_or_create(
                            content_type=content_type,
                            object_id=instance.pk,
                            field=f,
                            defaults={
                                'processor': processor,
                                'content': val,
                            }
                        )
            if created:
                setattr(instance, f, st.render())
                dirty = True

        if dirty or force_save:
            instance.__class__.objects.filter(pk=instance.pk).update(
                **dict( (f, getattr(instance, f)) for f in fields )
            )

    def extract_from_model(self, model, processor, fields):
        if not fields:
            return

        ct = ContentType.objects.get_for_model(model)

        for m in model._default_manager.all().iterator():
            self.extract_from_instance(m, processor, fields, ct)


class SourceText(models.Model):
    """
    Source text is plain text with processor-specific formatting inputted by user.
    """

    processor = models.ForeignKey(TextProcessor)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    field = models.CharField(max_length=64)
    target = GenericForeignKey('content_type', 'object_id')

    modification_time = models.DateTimeField(auto_now=True)

    content = models.TextField()

    objects = SourceTextManager()

    def __unicode__(self):
        return u"Source text of %s '%s' %s" % (self.content_type, self.target, self.field)

    @property
    def target_field(self):
        return getattr(self.target, self.field)

    def render(self):
        if not self.content:
            return ''
        return self.processor.convert(self.content)

    class Meta:
        unique_together = (('content_type', 'object_id', 'field'),)
        verbose_name = (_('Text source'))
        verbose_name_plural = (_('Text sources'))


def delete_listener(sender, instance, **kwargs):
    SourceText.objects.delete_for_object(instance)


signals.post_delete.connect(receiver=delete_listener, weak=False)
