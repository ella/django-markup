from djangosanetesting.cases import DatabaseTestCase
from djangomarkup.models import TextProcessor

class TestProcessors(DatabaseTestCase):
    def setUp(self):
        self.processor = TextProcessor(
            function = "unit_project.helpers.dummy_processor",
            name = "dummy",
            processor_options = ""
        )

    def test_conversion_executes_right_function(self):
        self.assert_equals(u"Hey", self.processor.convert(u"Hey"))