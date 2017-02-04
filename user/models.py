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
    grad_year_choices = (
        ("2017", "2017"),
        ("2018", "2018"),
        ("2019", "2019"),
        ("2020", "2020"),
    )

    university_choices = (
        ("Vellore Institute of Technology, Chennai", "Vellore Institute of Technology, Chennai"),
        ("Vellore Institute of Technology, Vellore", "Vellore Institute of Technology, Vellore"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=240, blank=True, default="")
    location = models.CharField(max_length=30, blank=True, default="")
    age = models.PositiveSmallIntegerField()
    course = models.CharField(max_length=6, choices=course_choices, default="B.Tech")
    school = models.CharField(max_length=6, choices=school_choices, default="SCSE")
    grad_year = models.CharField(max_length=6, choices=grad_year_choices)
