from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from ask.models import question
from django.contrib.auth.models import User
# Create your models here.


class answer(models.Model):
    question = models.ForeignKey(question)
    description = models.TextField()
    answer_author = models.CharField("Author", max_length=100, default="anon")
    created_time = models.DateTimeField(default=timezone.now)
    edited_time = models.DateTimeField(default=timezone.now, editable=True)
    edited = models.BooleanField(default=False)
    ups = models.ManyToManyField(User, related_name='upvotes')
    downs = models.ManyToManyField(User, related_name='downvotes')

    def __str__(self):
        return (self.description)

    def get_time(self):
        t = timezone.localtime(self.created_time)
        return "{}-{}-{} {}:{}".format(t.day, t.month, t.year, t.hour, t.minute)

    def get_edited_time(self):
        t = timezone.localtime(self.edited_time)
        return "{}-{}-{} {}:{}".format(t.day, t.month, t.year, t.hour, t.minute)

    def set_edited_time(self):
        self.edited = True
        self.edited_time = timezone.now()
