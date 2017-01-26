from django.db import models
from django.contrib.auth.models import User
# Signal Modules
from django.db.models.signals import post_save
from django.dispatch import receiver
# Form Modules
from django.forms import ModelForm


class student(models.Model):
    course_choices = (
        ("B.Tech", "B.Tech"),
        ("M.Tech", "M.Tech"),
        ("F.Tech", "F.Tech"),
        ("B.Law", "B.Law"),
    )
    school_choices = (
        ("SCSE", "SCSE"),
        ("SENSE", "SENSE"),
        ("SAS", "SAS"),
        ("SELECT", "SELECT"),
        ("SMBS", "SMBS"),
        ("VITBS", "VITBS"),
        ("VITSOL", "VITSOL"),
        ("VFIT", "VFIT"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=240, blank=True, default="")
    location = models.CharField(max_length=30, blank=True, default="")
    age = models.PositiveSmallIntegerField()
    course = models.CharField(max_length=6, choices=course_choices, default="B.Tech")
    school = models.CharField(max_length=6, choices=school_choices, default="SCSE")

