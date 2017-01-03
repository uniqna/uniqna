from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import render
from ask.forms import ask_form


def ask(request):
    if request.user.is_authenticated:
        username = request.user.username
        unsubmitted_form = ask_form()
        return render(request,
                      'ask_templates/ask.html',
                      {'username': username,
                       'form': unsubmitted_form})
    else:
        return HttpResponseRedirect(reverse('home'))


def submit(request):
    if request.method == 'POST' and request.POST:
        submitted_form = ask_form(request.POST)
        if submitted_form.is_valid():
            instance = submitted_form.save()
            question_id = instance.pk
            return HttpResponseRedirect("/thread/" + str(question_id))
        else:
            return HttpResponse('<p>Failed</p>')
    else:
        return HttpResponseRedirect(reverse('home'))
