from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
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
    all_answers = answer.objects.filter(question=thread_id)
    return render(request,
                  'thread_templates/thread.html',
                  {'question': question_requested,
                   'username': username,
                   'form': unsubmitted_answer,
                   'all_answers': all_answers})


def submit_answer(request, question_id):
    if request.method == 'POST' and request.POST:
        question_answered = get_object_or_404(question, pk=question_id)
        submitted_answer = answer_form(request.POST)
        if submitted_answer.is_valid():
            instance = submitted_answer.save(commit=False)
            instance.question = question_answered
            instance.answer_author = request.user.username
            instance.save()
            question_answered.answers = answer.objects.filter(question=question_id).count()
            question_answered.save()
            return HttpResponseRedirect("/thread/" + str(question_id))


def delete_question(request, thread_id):
    try:
        thread_id = int(thread_id)
    except ValueError:
        raise Http404()
    username = request.user.username
    question_requested = question.objects.get(id=thread_id)
    author = question_requested.author
    if author == username:
        question_requested.delete()
        answer.objects.filter(question=thread_id).delete()
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('home'))


def delete_answer(request, thread_id, answer_id):
    try:
        thread_id = int(thread_id)
    except ValueError:
        raise Http404()
    username = request.user.username
    answer_requested = answer.objects.get(id=answer_id)
    author = answer_requested.answer_author
    if author == username:
        answer_requested.delete()
        return HttpResponseRedirect("/thread/" + str(thread_id))
    else:
        return HttpResponseRedirect(reverse('home'))
