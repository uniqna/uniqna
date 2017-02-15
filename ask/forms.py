from django import forms
from ask.models import question


class ask_form(forms.ModelForm):

    class Meta:
        model = question
        fields = ('title', 'description',)
