from django import forms
from django.contrib.auth.models import User
from user.models import student
import re


class registration(forms.Form):
    username = forms.CharField(min_length=4, max_length=15)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    bio = forms.CharField(max_length=240)
    university = forms.ChoiceField(student.university_choices)
    course = forms.ChoiceField(student.course_choices)
    school = forms.ChoiceField(student.school_choices)
    grad_year = forms.ChoiceField(student.grad_year_choices)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=self.cleaned_data['username'].lower()).exists():
            raise forms.ValidationError(
                'Username "%s" is already in use.' % username)
        if re.match(r'^[_a-zA-Z0-9]{4,15}$', username):
            return username
        else:
            raise forms.ValidationError(
                'Username not valid.\nOnly use alphabets, numbers and underscore.')

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match.")
        return password2


class editForm(forms.Form):
    email = forms.CharField(required=True)
    bio = forms.CharField(max_length=240)
    university = forms.ChoiceField(student.university_choices)
    course = forms.ChoiceField(student.course_choices)
    school = forms.ChoiceField(student.school_choices)
    grad_year = forms.ChoiceField(student.grad_year_choices)


class changePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 != password2:
            raise forms.ValidationError("The passwords do not match.")
        return password2


class emailForm(forms.Form):
    email = forms.EmailField(required=True)
