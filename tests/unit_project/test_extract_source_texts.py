from djangomarkup.management.commands.extract_source_texts import get_fields_to_extract, Command

from djangosanetesting.cases import UnitTestCase

class TestArgsParsing(UnitTestCase):
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


class TestCommand(UnitTestCase):
    def setUp(self):
        self.command = Command()

    def test_fails_for_no_input(self):
        self.assert_equals(None, self.command.handle())

    def test_fails_for_incorrect_processor(self):
        self.assert_equals(None, self.command.handle('not-a-processor'))

    def test_fails_for_incorrect_fields(self):
        self.assert_equals(None, self.command.handle('markdown', 'not_a.model:field'))

    def test_works_for_no_fields(self):
        self.assert_equals(0, self.command.handle('markdown'))

    def test_works_with_correct_params(self):
        self.assert_equals(0, self.command.handle('markdown', 'contenttypes.contenttype:app_label'))

