from django import forms
from django.contrib.auth.models import User
from user.models import student
import re


class registration(forms.Form):
    username = forms.CharField(min_length=4)
    email = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    bio = forms.CharField(max_length=240)
    university = forms.ChoiceField(student.university_choices)
    age = forms.IntegerField(min_value=0, max_value=99)
    course = forms.ChoiceField(student.course_choices)
    school = forms.ChoiceField(student.school_choices)
    grad_year = forms.ChoiceField(student.grad_year_choices)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError('Username "%s" is already in use.' % username)
        if re.match(r'^[_a-zA-Z0-9]{4,15}$', username):
            return username
        else:
            raise forms.ValidationError('Username not valid.\nOnly use alphabets, numbers and underscore!!!')

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2
