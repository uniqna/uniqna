from django import forms

from post.models import Question


class post_form(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('title', 'description', )
