import datetime
from django.db import models

class Sources(models.Model):
    source_name = models.CharField(max_length=100)
    source_url = models.CharField(max_length=255, blank=True)

class Tags(models.Model):
    tag_name = models.CharField(max_length=50)

class News(models.Model):
    heading = models.CharField(max_length=255)
    news_text = models.TextField()
    source = models.ForeignKey(Sources, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, related_name='news')
