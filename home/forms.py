from django import forms
from django.contrib.auth.models import User


class registration(forms.Form):
    username = forms.CharField(min_length=4)
    email = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError('Username "%s" is already in use.' % username)
        return username

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2


class loginForm(forms.Form):
    username = forms.CharField(label="Username", min_length=4)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
