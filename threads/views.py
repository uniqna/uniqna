from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from threads.forms import answer_form
from threads.models import answer
from ask.models import question
from datetime import datetime
import markdown2
from root.algorithms import vote_score
from user.models import Answered
from django.contrib.auth.models import User


def thread(request, thread_id):
    try:
        thread_id = int(thread_id)
    except ValueError:
        raise Http404()
    username = request.user.username
    question_requested = get_object_or_404(question, pk=thread_id)
    description = markdown2.markdown(question_requested.description)
    unsubmitted_answer = answer_form()
    question_id = question_requested.pk
    all_answers = answer.objects.filter(question=thread_id).order_by("-score")
    for x in all_answers:
        x.description = markdown2.markdown(x.description)
    return render(request,
                  'thread_templates/thread.html',
                  {'question': question_requested,
                   'description': description,
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
            ans_notif = Answered()
            ans_notif.theanswer = instance
            ans_notif.save()
            question_author = get_object_or_404(User, username=question_answered.author)
            question_author.notifications.answers.add(ans_notif)
            return HttpResponseRedirect("/thread/" + str(question_id))


def delete_question(request, thread_id):
    try:
        thread_id = int(thread_id)
    except ValueError:
        raise Http404()
    username = request.user.username
    question_requested = get_object_or_404(question, pk=thread_id)
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
        answer_id = int(answer_id)
    except ValueError:
        raise Http404()
    username = request.user.username
    question_requested = get_object_or_404(question, pk=thread_id)
    answer_requested = answer.objects.get(id=answer_id)
    author = answer_requested.answer_author
    if author == username:
        answer_requested.delete()
        question_requested.answers = answer.objects.filter(question=thread_id).count()
        question_requested.save()
        return HttpResponseRedirect("/thread/" + str(thread_id))
    else:
        return HttpResponseRedirect(reverse('home'))


def edit_answer(request, thread_id, answer_id):
    try:
        thread_id = int(thread_id)
        answer_id = int(answer_id)
    except ValueError:
        raise Http404()
    answer_requested = get_object_or_404(answer, pk=answer_id)
    author = answer_requested.answer_author
    if author == request.user.username:
        description = answer_requested.description
        data = {'description': description}
        prefilled_form = answer_form(data)
        return render(request,
                      'edit_templates/edit.html',
                      {'username': request.user.username,
                       'form': prefilled_form,
                       'thread_id': thread_id,
                       'answer_id': answer_id})
    else:
        return HttpResponseRedirect(reverse('home'))


def edit_answer_submit(request, thread_id, answer_id):
    try:
        thread_id = int(thread_id)
        answer_id = int(answer_id)
    except ValueError:
        raise Http404()
    if request.method == 'POST' and request.POST:
        answer_requested = get_object_or_404(answer, pk=answer_id)
        edited_answer = answer_form(request.POST)
        if edited_answer.is_valid():
            updated_answer = edited_answer.save(commit=False)
            answer_requested.description = updated_answer.description
            answer_requested.set_edited_time()
            answer_requested.save()
        return HttpResponseRedirect("/thread/" + str(thread_id))
    else:
        return HttpResponseRedirect(reverse('home'))


def mark_answer_solved(request, thread_id):
    try:
        thread_id = int(thread_id)
    except ValueError:
        raise Http404()
    username = request.user.username
    question_requested = get_object_or_404(question, pk=thread_id)
    author = question_requested.author
    if author == username:
        question_requested.solved = True
        question_requested.save()
        return redirect('/thread/' + str(thread_id) + '/')
    else:
        return HttpResponseRedirect(reverse('home'))
