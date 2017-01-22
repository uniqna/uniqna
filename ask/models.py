from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from root.algorithms.popularity import _popularity


class ManagerExtender(models.Manager):
    def PopUpdate(self):
        for q in self.all():
            q.set_popularity()


class question(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    answers = models.IntegerField(default=0)
    author = models.CharField(max_length=100, default="anonymous")
    created_time = models.DateTimeField(default=timezone.now)
    ups = models.ManyToManyField(User, related_name='question_upvotes')
    downs = models.ManyToManyField(User, related_name='question_downvotes')
    popularity = models.DecimalField(default=0, max_digits=20, decimal_places=17)
    points = models.IntegerField(default=0)
    solved = models.BooleanField(default=False)
    objects = ManagerExtender()

    def __str__(self):
        return (self.title)

    def get_time(self):
        t = timezone.localtime(self.created_time)

        return "{}-{}-{} {}:{}".format(t.day, t.month, t.year, t.hour, t.minute)

    def set_popularity(self):
        self.popularity = _popularity(self)
        self.save()
