from django.db import models

class Article(models.Model):
    text = models.CharField(max_length=255)

    def __unicode__(self):
        return self.text