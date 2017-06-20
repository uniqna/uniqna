from django import forms

from threads.models import Answer


class reply_form(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('description',)
