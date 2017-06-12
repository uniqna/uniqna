from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from ask.models import question
from django.contrib.auth.models import User
from root.algorithms import vote_score
from mptt.models import MPTTModel, TreeForeignKey


class ManagerExtender(models.Manager):
    def ScoreUpdate(self):
        print("score Updating")
        for a in self.all():
            a.set_score()


class answer(MPTTModel):
    question = models.ForeignKey(question)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    metatype = models.CharField(max_length=20, default="question", blank=False)
    description = models.TextField(blank=True)
    answer_author = models.CharField("Author", max_length=100, default="anon")
    created_time = models.DateTimeField(default=timezone.now)
    edited_time = models.DateTimeField(default=timezone.now, editable=True)
    edited = models.BooleanField(default=False)
    ups = models.ManyToManyField(User, related_name='upvotes', blank=True)
    downs = models.ManyToManyField(User, related_name='downvotes', blank=True)
    points = models.IntegerField(default=1)
    score = models.DecimalField(default=0, max_digits=20, decimal_places=17)
    objects = ManagerExtender()

    def __str__(self):
        return str(self.description)

    def get_absolute_url(self):
        url = self.question.get_absolute_url()
        if self.parent:
            url += "/reply/{}"
        else:
            url += "/#a{}"
        return url.format(self.id)

    def get_time(self):
        t = timezone.localtime(self.created_time)
        return "{}-{}-{} {}:{}".format(t.day, t.month, t.year, t.hour, t.minute)

    def get_edited_time(self):
        t = timezone.localtime(self.edited_time)
        return "{}-{}-{} {}:{}".format(t.day, t.month, t.year, t.hour, t.minute)

    def set_edited_time(self):
        self.edited = True
        self.edited_time = timezone.now()

    def set_score(self):
        self.points = self.ups.count() - self.downs.count()
        self.score = vote_score.confidence(
            self.ups.count(), self.downs.count())
        self.save()

    class MPTTMeta:
        order_insertion_by = ['-score']
