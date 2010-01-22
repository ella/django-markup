from django.core.management.base import NoArgsCommand
from django.db import transaction

from djangomarkup.models import SourceText

class Command(NoArgsCommand):
    help = 'Clean SourceText orphans'

    @transaction.commit_manually
    def handle_noargs(self, **options):

        transaction.managed()

        qs = SourceText.objects.all()
        counter = 0
        print "%d total SourceText entries." % qs.count()

        for srctext in qs:
            if not srctext.target:
                srctext.delete()
                counter += 1

        transaction.commit()

        print "%d orphaned SourceText was removed." % counter
        return 0
