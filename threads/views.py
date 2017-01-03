from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from ask.models import question


def thread(request, thread_id):
    try:
        thread_id = int(thread_id)
    except ValueError:
        raise Http404()
    username = request.user.username
    question_requested = question.objects.get(id=thread_id)
    return render(request,
                  'thread_templates/thread.html',
                  {'question': question_requested, 'username': username})
