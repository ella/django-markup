from djangosanetesting.cases import DatabaseTestCase

from djangomarkup.fields import RichTextField
from djangomarkup.models import SourceText

from exampleapp.models import Article

class TestRichTextField(DatabaseTestCase):

    def setUp(self):
        super(TestRichTextField, self).setUp()
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

