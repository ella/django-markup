from django.db import models
#from djangomarkup.models import RichTextField

class Article(models.Model):
#    text = RichTextField(max_length=255, syntax="markdown")
    text = models.TextField(max_length=255)
    email = models.EmailField()

    def __unicode__(self):
        return self.text
