from django.db import models

class Sources(models.Model):
    source_name = models.CharField(max_length=100)
    source_url = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.source_name

class Tags(models.Model):
    tag_name = models.CharField(max_length=50)
    def __str__(self):
        return self.tag_name

class News(models.Model):
    heading = models.CharField(max_length=255)
    news_text = models.TextField()
    source = models.ForeignKey(Sources, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, related_name='news')
    def __str__(self):
        return self.heading