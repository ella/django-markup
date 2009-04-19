from ella import newman
from djangomarkup.models import SourceText, TextProcessor

newman.site.register([SourceText, TextProcessor])
