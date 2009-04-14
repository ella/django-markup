from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

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
        if not hasattr(self, '_function'):
            mod = __import__('.'.join(self.function.split('.')[:-1]), {}, {}, [self.function.split('.')[-1]])
            self._function = getattr(mod, self.function.split('.')[-1])
        return self._function

    def convert(self, src_txt):
        return self.get_function()(src_txt)

    class Meta:
        verbose_name = (_('Text processor'))
        verbose_name_plural = (_('Text processors'))


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

    def __unicode__(self):
        return u"Source text for %s:%s" % (self.target, self.field)

    @property
    def target_field(self):
        return getattr(self.target, self.field)

    def render(self):
        return self.processor.convert(self.content)

    class Meta:
        unique_together = (('content', 'object_id', 'field'),)
        verbose_name = (_('Text source'))
        verbose_name_plural = (_('Text sources'))
