from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import render
from ask.forms import ask_form
from ask.models import question, tag


def ask(request):
    if request.user.is_authenticated:
        username = request.user.username
        unsubmitted_form = ask_form()
        return render(request,
                      'ask_templates/ask.html',
                      {'username': username,
                       'tags': tag.objects.all(),
                       'form': unsubmitted_form})
    else:
        return HttpResponseRedirect(reverse('home'))


def submit(request):
    if request.method == 'POST' and request.POST:
        submitted_form = ask_form(request.POST)
        if submitted_form.is_valid():
            instance = submitted_form.save(commit=False)
            instance.author = request.user.username
            instance.save()
            selectedtags = request.POST['selectedtags']
            taglist = selectedtags.split(",")
            print(taglist)
            for tagname in taglist:
                selected_tag = tag.objects.get(name=tagname)
                instance.tags.add(selected_tag)
            question_id = instance.pk
            return HttpResponseRedirect("/thread/" + str(question_id))
        else:
            return HttpResponse('<p>Failed</p>')
    else:
        return HttpResponseRedirect(reverse('home'))
