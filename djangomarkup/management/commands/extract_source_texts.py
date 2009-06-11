from django.core.management.base import BaseCommand
from django.db.models import get_model
from django.db.models.fields import FieldDoesNotExist

from djangomarkup.models import TextProcessor, SourceText


def get_fields_to_extract(fields):
    to_extract = {}
    for f in fields:
        if ':' not in f:
            print Command.args
            return

        model_name, field_name = f.split(':', 1)

        if '.' not in model_name:
            print Command.args
            return

        model = get_model(*model_name.split('.', 1))

        if not model:
            print 'Model with name %r does not exist.' % model_name
            return

        try:
            field = model._meta.get_field(field_name)
        except FieldDoesNotExist, e:
            print 'Field with name %r does not exist on model %s.' % (field_name, model_name)
            return

        to_extract.setdefault(model_name, []).append(field_name)

    return to_extract

class Command(BaseCommand):
    help = 'Migrate selected fields to django-markup'
    args = 'markup app_label.model:field [app_label.model:field ...]'
    def handle(self, *args, **options):
        if not args:
            print self.args
            return

        markup, fields = args[0], args[1:]

        try:
            procesor = TextProcessor.objects.get(name=markup)
        except TextProcessor.DoesNotExist, e:
            print 'Procesor with name %r not found.' % markup
            return

        to_extract = get_fields_to_extract(fields)

        if to_extract is None:
            return

        for model_name, fields in to_extract.items():
            model = get_model(*model_name.split('.', 1))
            SourceText.objects.extract_from_model(model, procesor, fields)

        return 0
