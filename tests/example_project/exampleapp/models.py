from django.db import models

class Articles(models.Model):
    text = models.CharField(max_length=255)
