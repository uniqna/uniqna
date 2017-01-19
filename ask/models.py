from django.db import models
from django.utils import timezone


class question(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    answers = models.IntegerField(default=0)
    author = models.CharField(max_length=100, default="anonymous")
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (self.title)

    def get_time(self):
        t = timezone.localtime(self.created_time)

        return "{}-{}-{} {}:{}".format(t.day, t.month, t.year, t.hour, t.minute)
