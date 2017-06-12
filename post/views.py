from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from post.forms import post_form
from post.models import Channel


def ask(request):
    if request.user.is_authenticated:
        metatype = "question"
        unsubmitted_form = post_form()
        return render(request,
                      'post_templates/post.html',
                      {'metatype': metatype,
                       'tags': Channel.objects.all(),
                       'form': unsubmitted_form})
    else:
        return HttpResponseRedirect(reverse('home'))


def discuss(request):
    if request.user.is_authenticated:
        metatype = "discussion"
        unsubmitted_form = post_form()
        return render(request,
                      'post_templates/post.html',
                      {'metatype': metatype,
                       'tags': Channel.objects.all(),
                       'form': unsubmitted_form})
    else:
        return HttpResponseRedirect(reverse('home'))


def submit(request, metatype):
    if request.method == 'POST' and request.POST:
        submitted_form = post_form(request.POST)
        if submitted_form.is_valid():
            instance = submitted_form.save(commit=False)
            instance.author = request.user.username
            instance.metatype = metatype
            instance.save()
            instance.ups.add(request.user)
            if request.POST['selectedtags']:
                selectedtags = request.POST['selectedtags']
                taglist = selectedtags.split(",")
                taglist = [x.lower() for x in taglist if x != '']
                for tagname in taglist:
                    selected_tag = Channel.objects.get(name=tagname)
                    instance.tags.add(selected_tag)
            return HttpResponseRedirect("/thread/" + str(instance.pk))
        else:
            return render(request,
                          "post_templates/post.html",
                          {"username": request.user.username,
                           "tags": Channel.objects.all(),
                           "form": submitted_form,
                           "errors": submitted_form.errors})
    else:
        return HttpResponseRedirect(reverse('home'))
