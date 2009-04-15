from django.contrib.sites.admin import admin
from django.contrib.admin.options import ModelAdmin

from djangomarkup.models import SourceText, TextProcessor
from djangomarkup.fields import RichTextField

class SourceTextOptions(ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "content":
            kwargs.update({
                'required': not db_field.blank,
                'label': db_field.verbose_name,
                'field_name': db_field.name,
                'instance': kwargs.get('instance', None),
                'model': self.model,
            })
            return RichTextField(**kwargs)
        return super(SourceTextOptions, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(SourceText, SourceTextOptions)
admin.site.register(TextProcessor)
