from django.contrib.admin.options import ModelAdmin
from django.contrib.sites.admin import admin

from djangomarkup.models import SourceText, TextProcessor
from djangomarkup.fields import RichTextField

class RichTextOptions(ModelAdmin):
    rich_text_field_names = []
    syntax_processor_name = "markdown"
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.rich_text_field_names:
            kwargs.update({
                'required': not db_field.blank,
                'label': db_field.verbose_name,
                'field_name': db_field.name,
                'instance': kwargs.get('instance', None),
                'model': self.model,
                'syntax_processor_name' : self.syntax_processor_name,
            })
            return RichTextField(**kwargs)
        return super(RichTextOptions, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(SourceText)
admin.site.register(TextProcessor)
