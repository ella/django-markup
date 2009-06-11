from djangosanetesting.cases import UnitTestCase, DatabaseTestCase

from django.contrib.contenttypes.models import ContentType

from djangomarkup.management.commands.extract_source_texts import get_fields_to_extract, Command
from djangomarkup.models import SourceText, TextProcessor

from exampleapp.models import Article

class TestArgsParsing(UnitTestCase):
    def setUp(self):
        super(TestArgsParsing, self).setUp()
        self.command = Command()

    def test_return_empty_dict_on_empty_input(self):
        self.assert_equals({}, get_fields_to_extract([]))

    def test_fails_on_invalid_model(self):
        self.assert_equals(None, get_fields_to_extract(['not_a.model:field']))

    def test_fails_on_non_existent_field(self):
        self.assert_equals(None, get_fields_to_extract(['contenttypes.contenttype:not_a_field']))

    def test_fails_without_colon(self):
        self.assert_equals(None, get_fields_to_extract(['aljshfdlsah']))

    def test_fails_without_dot(self):
        self.assert_equals(None, get_fields_to_extract(['aljshfdlsah:field']))

    def test_works_for_single_input(self):
        self.assert_equals(
                {'contenttypes.contenttype': ['name']},
                get_fields_to_extract(['contenttypes.contenttype:name'])
            )

    def test_groups_results_by_model(self):
        self.assert_equals(
                {'contenttypes.contenttype': ['name', 'app_label']},
                get_fields_to_extract(['contenttypes.contenttype:name', 'contenttypes.contenttype:app_label'])
            )

    def test_fails_for_no_input(self):
        self.assert_equals(None, self.command.handle())

    def test_fails_for_incorrect_processor(self):
        self.assert_equals(None, self.command.handle('not-a-processor'))

    def test_fails_for_incorrect_fields(self):
        self.assert_equals(None, self.command.handle('markdown', 'not_a.model:field'))

    def test_works_for_no_fields(self):
        self.assert_equals(0, self.command.handle('markdown'))

class TestExtraction(DatabaseTestCase):
    def setUp(self):
        super(TestExtraction, self).setUp()
        self.processor = TextProcessor.objects.get(name='markdown')

    def test_command_works_with_correct_params(self):
        command = Command()
        self.assert_equals(0, command.handle('markdown', 'contenttypes.contenttype:app_label'))

    def test_no_source_texts_created_if_no_fields_given(self):
        SourceText.objects.extract_from_model(ContentType, self.processor, [])
        self.assert_equals(0, SourceText.objects.count())

    def test_extract_creates_source_texts_for_specified_field(self):
        SourceText.objects.extract_from_model(ContentType, self.processor, ['app_label'])
        self.assert_equals(ContentType.objects.count(), SourceText.objects.count())

    def test_extract_creates_source_texts_for_specified_fields(self):
        SourceText.objects.extract_from_model(ContentType, self.processor, ['app_label', 'name',])
        self.assert_equals(ContentType.objects.count()*2, SourceText.objects.count())

    def test_fields_on_model_are_migrated(self):
        a = Article.objects.create(text='*bold*')
        SourceText.objects.extract_from_model(Article, self.processor, ['text'])

        self.assert_equals(1, SourceText.objects.count())
        st = SourceText.objects.all()[0]
        self.assert_equals(a, st.target)
        self.assert_equals('<p><em>bold</em></p>\n', st.target_field)
        self.assert_equals(a.text, st.content)

