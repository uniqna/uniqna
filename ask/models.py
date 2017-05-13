from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from root.algorithms.popularity import _popularity
from django.template.defaultfilters import slugify


class ManagerExtender(models.Manager):
    def PopUpdate(self):
        for q in self.all():
            q.set_popularity()


class tag(models.Model):
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name


class question(models.Model):
    metatype = models.CharField(max_length=20, default="question", blank=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    answers = models.IntegerField(default=0)
    author = models.CharField(max_length=100, default="anonymous")
    created_time = models.DateTimeField(default=timezone.now)
    ups = models.ManyToManyField(User, related_name='question_upvotes', blank=True)
    downs = models.ManyToManyField(User, related_name='question_downvotes', blank=True)
    hot = models.DecimalField(default=1000.123, max_digits=11, decimal_places=7, blank=True)
    points = models.IntegerField(default=1)
    solved = models.BooleanField(default=False)
    tags = models.ManyToManyField(tag, blank=True)
    flair_icon = models.CharField(max_length=25, null=True)
    flair = models.CharField(max_length=180, null=True)
    objects = ManagerExtender()

    def __str__(self):
        return (self.title)

    def get_time(self):
        t = timezone.localtime(self.created_time)
        return "{}-{}-{} {}:{}".format(t.day, t.month,
                                       t.year, t.hour,
                                       t.minute)

    def set_popularity(self):
        ups = self.ups.count()
        downs = self.downs.count()
        self.hot = _popularity(ups, downs, self.created_time)
        self.save()

    def get_absolute_url(self):
        return reverse('thread', args=[str(self.pk), slugify(self.title)])
