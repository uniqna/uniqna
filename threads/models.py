from __future__ import unicode_literals

from django.db import models
from ask.models import question

# Create your models here.


class answer(models.Model):
    question = models.ForeignKey(question)
    description = models.TextField()
    answer_author = models.CharField("Author", max_length=100, default="anonymous")

    def __str__(self):
        return (self.description)
