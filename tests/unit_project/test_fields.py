# -*- coding: utf-8 -*-
from xml.dom import ValidationErr
from djangosanetesting.cases import UnitTestCase, DatabaseTestCase

from djangomarkup.fields import RichTextField
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
        self.article = Article.objects.create(text=self.text)
        self.field = RichTextField(
            instance = self.article,
            model = Article,
            syntax_processor_name = "markdown",
            field_name = "text",
            required = True,
            label = "Text"
        )

    def test_value_stored(self):
        self.field.clean(value=self.text)
        self.assert_equals(self.text, SourceText.objects.all()[0].content)
