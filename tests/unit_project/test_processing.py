# -*- coding: utf-8 -*-
from djangosanetesting.cases import UnitTestCase
from djangomarkup.models import TextProcessor
from djangomarkup.processors import ProcessorConfigurationError, ProcessorError

class TestProcessors(UnitTestCase):

    def test_conversion_executes_right_function(self):
        processor = TextProcessor(
            function = "unit_project.helpers.dummy_processor",
            name = "dummy",
            processor_options = ""
        )
        self.assert_equals(u"Hey", processor.convert(u"Hey"))

    def test_nonexisting_processor_raises_improperly_configured(self):
        bad_processor = TextProcessor(
            function = "non.existing.bad.processor.function",
            name = "nonexisting processor",
            processor_options = "",
        )
        self.assert_raises(ProcessorConfigurationError, bad_processor.convert, u"Hey!")

    def test_nonexisting_processor_raises_improperly_configured_when_module_exists(self):
        bad_processor = TextProcessor(
            function = "unit_project.helpers.nonexisting_processor",
            name = "nonexisting processor",
            processor_options = "",
        )
        self.assert_raises(ProcessorConfigurationError, bad_processor.convert, u"Hey!")

    def test_processor_errors_raises_processor_exception(self):
        processor = TextProcessor(
            function = "unit_project.helpers.dummy_processor_always_raising_value_error",
            name = "dummy",
            processor_options = ""
        )
        self.assert_raises(ProcessorError, processor.convert, u"Hey")
