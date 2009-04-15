from django.contrib.sites.admin import admin
from djangomarkup.models import SourceText, TextProcessor

admin.site.register(SourceText)
admin.site.register(TextProcessor)
