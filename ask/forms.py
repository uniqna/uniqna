from django import forms
from ask.models import question
from trumbowyg.widgets import TrumbowygWidget


class ask_form(forms.ModelForm):

    class Meta:
        model = question
        fields = ('title', 'description',)
        widgets = {'id_description': TrumbowygWidget(), }
