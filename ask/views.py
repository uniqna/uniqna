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
                      {'tags': tag.objects.all(),
                       'form': unsubmitted_form})
    else:
        return HttpResponseRedirect(reverse('home'))


def submit(request):
    if request.method == 'POST' and request.POST:
        submitted_form = ask_form(request.POST)
        if request.POST["new_tag"]:
            t = tag()
            t.name = request.POST['new_tag']
            t.save()
            return render(request, "ask_templates/ask.html", {'form': submitted_form, 'tags': tag.objects.all()})
        if submitted_form.is_valid():
            instance = submitted_form.save(commit=False)
            instance.author = request.user.username
            instance.save()
            # Get the selected checkbox items value from the POST request as a list
            taglist = request.POST.getlist('tag')
            # The checkbox value is the primary key of the tag
            for tag_id in taglist:
                # Get the tag using the pk
                selected_tag = tag.objects.get(pk=tag_id)
                instance.tags.add(selected_tag)
            question_id = instance.pk
            return HttpResponseRedirect("/thread/" + str(question_id))
        else:
            return HttpResponse('<p>Failed</p>')
    else:
        return HttpResponseRedirect(reverse('home'))
