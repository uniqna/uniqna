from django.db import models
from rest_framework import serializers


class UsernameSnippet(models.Model):
	available = models.BooleanField()
