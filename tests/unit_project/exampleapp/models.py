from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255, blank=True, default='')
    text = models.CharField(max_length=255)
