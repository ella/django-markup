from django.contrib.sites.admin import admin

from djangomarkup.admin import RichTextModelAdmin

from exampleapp.models import Article


class ArticleOptions(RichTextModelAdmin):
    rich_text_field_names = ["text"]
    syntax_processor_name = "markdown"

admin.site.register(Article, ArticleOptions)
