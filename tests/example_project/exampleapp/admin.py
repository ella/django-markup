from django.contrib.sites.admin import admin

from djangomarkup.admin import RichTextOptions

from exampleapp.models import Article


class ArticleOptions(RichTextOptions):
    rich_text_field_names = ["text"]
    syntax_processor_name = "markdown"

admin.site.register(Article, ArticleOptions)
