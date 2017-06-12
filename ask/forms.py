from django import forms
from ask.models import Question


class ask_form(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('title', 'description',)
