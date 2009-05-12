# -*- coding: utf-8 -*-
from django.db.models import signals

from djangosanetesting.cases import UnitTestCase, DatabaseTestCase

from djangomarkup.fields import RichTextField, ListenerPostSave
from djangomarkup.models import SourceText

from exampleapp.models import Article

class TestRichTextFieldModifications(UnitTestCase):

    def setUp(self):
        super(TestRichTextFieldModifications, self).setUp()
        self.field = RichTextField(
            instance = Article(),
            model = Article,
            syntax_processor_name = "markdown",
            field_name = "text",
            required = True,
            label = "Text"
        )


    def test_retrieve_empty_source_for_empty_article(self):
        self.assert_equals(u'', self.field.get_source().content)

    def test_source_available_for_empty_article(self):
        self.assert_equals(u'', self.field.get_source_text())

    def test_render_available_for_empty_article(self):
        self.assert_equals(u'<p></p>', self.field.get_rendered_text().strip())

    def test_value_error_raised_when_accessing_source_without_instance(self):
        field = RichTextField(
            instance = None,
            model = Article,
            syntax_processor_name = "markdown",
            field_name = "text",
            required = True,
            label = "Text"
        )

        self.assert_raises(ValueError, field.get_source)

class TestRichTextFieldCleaning(DatabaseTestCase):
    def setUp(self):
        super(TestRichTextFieldCleaning, self).setUp()

        self.text = u"我说，你们听。"
        self.article = Article.objects.create(text=u"")
        self.field = RichTextField(
            instance = self.article,
            model = Article,
            syntax_processor_name = "markdown",
            field_name = "text",
            required = True,
            label = "Text"
        )

    def test_source_text_not_stored_on_form_clean(self):
        self.field.clean(value=self.text)
        self.assert_equals(0, len(SourceText.objects.all()))

#    def test_source_text_stored_on_update(self):
#        self.field.clean(value=self.text)
#        new_value = u"对不起"
#        self.field.clean(value=new_value)
#        self.assert_equals(new_value, SourceText.objects.all()[0].content)

    def test_render_retrieved(self):
        self.assert_equals(u"<p>%s</p>" % self.text, self.field.clean(value=self.text).strip())

    def test_source_stored_for_fresh_model(self):
        self.field = RichTextField(
            instance = None,
            model = Article,
            syntax_processor_name = "markdown",
            field_name = "text",
            required = True,
            label = "Text"
        )
        Article.objects.create(text=self.field.clean(value=self.text))
        self.assert_equals(self.text, SourceText.objects.all()[0].content)
    
    def test_empty_clean_same_as_render(self):
        self.field = RichTextField(
            instance = self.article,
            model = Article,
            syntax_processor_name = "markdown",
            field_name = "text",
            required = False,
            label = "Text"
        )
        self.assert_equals(self.field.get_rendered_text(), self.field.clean(u''))

    def test_deleting_article_deletes_source_text(self):
        self.field = RichTextField(
            instance = None,
            model = Article,
            syntax_processor_name = "markdown",
            field_name = "text",
            required = True,
            label = "Text"
        )
        a = Article.objects.create(text=self.field.clean(value=self.text))
        a.delete()

        self.assert_equals(0, SourceText.objects.count())


