from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from threads.forms import answer_form
from threads.models import answer
from ask.models import question
from datetime import datetime
from root.algorithms import vote_score
# Required REST modules
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AnswerSerializer

# Get the ups and down of an answer or send a vote


class VotesView(APIView):

    def get(self, request):
        answers = answer.objects.all()
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

    def post(self):
        pass


def thread(request, thread_id):
    try:
        thread_id = int(thread_id)
    except ValueError:
        raise Http404()
    username = request.user.username
    question_requested = get_object_or_404(question, pk=thread_id)
    unsubmitted_answer = answer_form()
    question_id = question_requested.pk
    all_answers = answer.objects.filter(question=thread_id).order_by("-score")
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


def vote(request, thread_id, answer_id, upordown):
    try:
        thread_id = int(thread_id)
        answer_id = int(answer_id)
    except ValueError:
        raise Http404()
    if request.user.is_authenticated:
        answer_instance = get_object_or_404(answer, pk=answer_id)
        if upordown == 'u':
            vote_on = answer_instance.ups
            vote_on_other = answer_instance.downs
        elif upordown == 'd':
            vote_on = answer_instance.downs
            vote_on_other = answer_instance.ups
        if request.user not in vote_on.all():
            vote_on.add(request.user)
            vote_on_other.remove(request.user)
        else:
            vote_on.remove(request.user)
        upvotes = answer_instance.ups.count()
        downvotes = answer_instance.downs.count()
        answer_instance.score = vote_score.confidence(upvotes, downvotes)
        answer_instance.save()
        return redirect('/thread/' + str(thread_id) + '/')
    else:
        return redirect('home')


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
