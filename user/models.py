from django.db import models
from django.contrib.auth.models import User
# Form Modules
from django.forms import ModelForm
# Notificaition modules
from threads.models import answer


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
    course = models.CharField(max_length=6, choices=course_choices, default="B.Tech")
    school = models.CharField(max_length=6, choices=school_choices, default="SCSE")
    grad_year = models.CharField(max_length=6, choices=grad_year_choices, default="2020")
    university = models.CharField(max_length=100, choices=university_choices)


class AnsweredNotifcation(models.Model):
    theanswer = models.ForeignKey(answer, related_name="writted_answer")
    read = models.BooleanField(default=False)


class Notification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    answers = models.ManyToManyField(AnsweredNotifcation, related_name="answered_questions")
