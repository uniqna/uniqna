from django import forms
from threads.models import answer
from tinymce.models import HTMLField


class answer_form(forms.ModelForm):

    class Meta:
        model = answer
        fields = ('description',)
