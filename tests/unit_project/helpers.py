from django.db.models import signals

def dummy_processor(text, **kwargs):
    return text

def dummy_processor_always_raising_value_error(text, **kwargs):
    raise ValueError()

class ExamplePostSave(object):
    def __init__(self, src_text):
        super(ExamplePostSave, self).__init__()
        self.src_text = src_text
        self.called = False

    def __call__(self, sender, signal, created, **kwargs):
        self.called = True
        signals.post_save.disconnect(receiver=self, sender=self.src_text.content_type.model_class())
