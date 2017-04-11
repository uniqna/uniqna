from django.db import models
from django.contrib.auth.models import User
# Form Modules
from django.forms import ModelForm
# Notification modules
from threads.models import answer


class ManagerExtender(models.Manager):
    def unread_count(self):
        unread_list = [1 for o in self.all() if not o.read]
        unread_count = int(sum(unread_list))
        return unread_count

    def sort_read(self):
        unsorted = self.all()
        srted = sorted(unsorted, key=lambda x: (
            x.theanswer.created_time, x.read), reverse=True)
        return srted


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
        ("V-SPARC", "V-SPARC"),
        ("SBST", "SBST"),
        ("SCALE", "SCALE"),
        ("SCOPE", "SCOPE"),
        ("SITE", "SITE"),
        ("SMEC", "SMEC"),
        ("SSL", "SSL"),
        ("LAW", "LAW"),
    )
    grad_year_choices = (
        ("2017", "2017"),
        ("2018", "2018"),
        ("2019", "2019"),
        ("2020", "2020"),
    )

    university_choices = (
        ("Vellore Institute of Technology, Chennai",
         "Vellore Institute of Technology, Chennai"),
        ("Vellore Institute of Technology, Vellore",
         "Vellore Institute of Technology, Vellore"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=15, default="")
    bio = models.CharField(max_length=240, blank=True, default="")
    course = models.CharField(
        max_length=6, choices=course_choices, default="B.Tech")
    school = models.CharField(
        max_length=6, choices=school_choices, default="SCSE")
    grad_year = models.CharField(
        max_length=6, choices=grad_year_choices, default="2020")
    university = models.CharField(max_length=100, choices=university_choices)


class Answered(models.Model):
    theanswer = models.ForeignKey(answer, related_name="writted_answer")
    read = models.BooleanField(default=False)
    objects = ManagerExtender()

    class Meta:
        ordering = ["-read"]


class Notifications(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    answers = models.ManyToManyField(
        Answered, related_name="answered_questions")
