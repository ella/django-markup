from django.contrib.sites.admin import admin
from django.contrib.admin.options import ModelAdmin

from djangomarkup.models import SourceText, TextProcessor

class SourceTextOptions(ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if dbfield.name == "content":
            return RichTextField()
        return super

admin.site.register(SourceText, SourceTextOptions)
admin.site.register(TextProcessor)
