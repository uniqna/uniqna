from django.db import models


class question(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    answers = models.IntegerField(default=0)
    author = models.CharField(max_length=100, default="anonymous")

    def __str__(self):
        return (self.title)
