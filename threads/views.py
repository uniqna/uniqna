from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from threads.forms import answer_form
from threads.models import answer
from ask.models import question



def thread(request, thread_id):
    try:
        thread_id = int(thread_id)
    except ValueError:
        raise Http404()
    username = request.user.username
    question_requested = question.objects.get(id=thread_id)
    unsubmitted_answer = answer_form()
    question_id = question_requested.pk
    return render(request,
                  'thread_templates/thread.html',
                  {'question': question_requested,
                   'username': username,
                   'form': unsubmitted_answer,})


def answer(request, question_id):
    if request.method == 'POST' and request.POST:
        question_answered = get_object_or_404(question, pk=question_id)
        submitted_answer = answer_form(request.POST)
        if submitted_answer.is_valid():
            instance = submitted_answer.save(commit=False)
            instance.question = question_answered
            instance.save()
            return HttpResponse("<p>Success!</p>")
