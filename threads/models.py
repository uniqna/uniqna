from __future__ import unicode_literals

from django.db import models
from ask.models import question
from datetime import datetime
# Create your models here.


class answer(models.Model):
    question = models.ForeignKey(question)
    description = models.TextField()
    answer_author = models.CharField("Author", max_length=100, default="anonymous")
    created_time = models.DateTimeField(auto_now_add=True)
    edited_time = models.DateTimeField(auto_now_add=True, editable=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return (self.description)

    def get_time(self):
        t = self.created_time
<<<<<<< HEAD
        return "{}-{}-{} {}:{}".format(t.day, t.month, t.year, t.hour, t.minute);

    def get_edited_time(self):
        t = self.edited_time
        return "{}-{}-{} {}:{}".format(t.day, t.month, t.year, t.hour, t.minute);

    def set_edited_time(self):
        self.edited = True
        self.edited_time = datetime.now();
=======
        return "{}-{}-{} {}:{}".format(t.day, t.month, t.year, t.hour, t.minute)

    def get_edited_time(self):
        t = self.edited_time
        return "{}-{}-{} {}:{}".format(t.day, t.month, t.year, t.hour, t.minute)

    def set_edited_time(self):
        self.edited = True
        self.edited_time = datetime.now()
>>>>>>> origin/timestamp-branch
