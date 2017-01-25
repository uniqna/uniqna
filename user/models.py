from django.db import models
from django.contrib.auth.models import User
# Signal Modules
from django.db.models.signals import post_save
from django.dispatch import receiver
# Form Modules
from django.forms import ModelForm


class student(models.Model):
    course_choices = (
        ("BT", "B.Tech"),
        ("MT", "M.Tech"),
        ("FT", "F.Tech"),
        ("BL", "B.Law"),
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
    course = models.CharField(max_length=5, choices=course_choices, default="BT")
    school = models.CharField(max_length=6, choices=school_choices, default="SCSE")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        student.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.student.save()


# Form Classes

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password"]


class ProfileForm(ModelForm):
    class Meta:
        model = student
        fields = ["age", "bio", "location", "course", "school"]
