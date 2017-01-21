from django import forms
from django.contrib.auth.models import User
import re


class registration(forms.Form):
    username = forms.CharField(min_length=4)
    email = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

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
