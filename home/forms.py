from django import forms
from django.contrib.auth.models import User

import re


class registration(forms.Form):
	username = forms.CharField(min_length=4, max_length=15, required=True)
	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput, required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
	bio = forms.CharField(max_length=256)

	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(
			username__iexact=self.cleaned_data['username'].lower()).exists():
			raise forms.ValidationError(
				'Username "%s" is already in use' % username)
		if re.match(r'^[_a-zA-Z0-9]{4,15}$', username):
			return username
		else:
			raise forms.ValidationError(
				'Username not valid.\nOnly use alphabets, numbers and underscore')

	def clean_confirm_password(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('confirm_password')
		if password1 != password2:
			raise forms.ValidationError("Your passwords do not match")
		return password2

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if (re.search(r'(vitstudent.ac.in)$', email)):
			if User.objects.filter(email=email).exists():
				raise forms.ValidationError('An account with that email ID already exists, so please log in fam :D')
			else:
				return email
		else:
			raise forms.ValidationError('Uh you need to enter your vit student email id')


class editForm(forms.Form):
	bio = forms.CharField(max_length=256)


class changePasswordForm(forms.Form):
	current_password = forms.CharField(widget=forms.PasswordInput, required=True)
	new_password = forms.CharField(widget=forms.PasswordInput, required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

	def clean_confirm_password(self):
		password1 = self.cleaned_data.get('new_password')
		password2 = self.cleaned_data.get('confirm_password')
		if password1 != password2:
			raise forms.ValidationError("Your passwords do not match")
		return self.cleaned_data


class emailForm(forms.Form):
	email = forms.EmailField(required=True)
