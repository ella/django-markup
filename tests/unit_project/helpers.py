from django.db.models import signals

def dummy_processor(text, **kwargs):
    return text

def dummy_processor_always_raising_value_error(text, **kwargs):
    raise ValueError()

