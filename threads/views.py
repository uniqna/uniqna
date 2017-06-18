from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import markdown2

from post.models import Question
from threads.forms import answer_form
from threads.models import Answer
from user.models import Notification


def thread(request, thread_id, slug):
	try:
		thread_id = int(thread_id)
	except ValueError:
		raise Http404()
	question_requested = get_object_or_404(Question, pk=thread_id)
	description = markdown2.markdown(
		question_requested.description,
		extras=["tables", "cuddled-lists"]
	)
	unsubmitted_answer = answer_form()
	Answer._tree_manager.rebuild()  # You rebuild the tree and then query.
	all_answers = Answer.objects.filter(
		question=question_requested).order_by('tree_id', 'lft')
	for x in all_answers:
		x.description = markdown2.markdown(
			x.description, extras=["tables", "cuddled-lists"])
	return render(
		request,
		'thread_templates/thread.html',
		{
			'question': question_requested,
			'description': description,
			'form': unsubmitted_answer,
			'nodes': all_answers
		})


def reply(request, thread_id, answer_id):
	try:
		answer_id = int(answer_id)
	except ValueError:
		raise Http404()
	parent_ques = get_object_or_404(Question, pk=thread_id)
	Answer._tree_manager.rebuild()
	answer_req = get_object_or_404(Answer, pk=answer_id)
	replies = answer_req.get_descendants(True)
	replies = replies.order_by('tree_id', 'lft')
	description = parent_ques.description
	return render(request, 'thread_templates/thread.html', {
		'question': parent_ques,
		'nodes': replies,
		'description': description,
		'reply': True
	})


def submit_answer(request, thread_id):
	if request.method == 'POST' and request.POST:
		question_answered = get_object_or_404(Question, pk=thread_id)
		question_metatype = question_answered.metatype
		submitted_answer = answer_form(request.POST)
		if submitted_answer.is_valid():
			instance = submitted_answer.save(commit=False)
			instance.question = question_answered
			instance.metatype = question_metatype
			instance.answer_author = request.user.username
			instance.save()
			instance.ups.add(request.user)
			question_answered.answers = Answer.objects.filter(
				question=thread_id).count()
			question_answered.save()
			question_author = get_object_or_404(
				User, username=question_answered.author)
			Notification.objects.create_answer_notification(
				question_author, instance)
			return HttpResponseRedirect(question_answered.get_absolute_url())


def submit_reply(request, answer_id):
	if request.method == "POST" and request.POST:
		parent = Answer.objects.filter(
			pk=answer_id).select_related('question')[0]
		question_instance = parent.question
		question_id = question_instance.pk
		submitted_reply = answer_form(request.POST)
		if submitted_reply.is_valid():
			reply = submitted_reply.save(commit=False)
			reply.parent = parent
			reply.question = parent.question
			reply.metatype = parent.question.metatype
			reply.answer_author = request.user.username
			reply.save()
			reply.ups.add(request.user)
			question_instance.answers = Answer.objects.filter(
				question=question_id).count()
			question_instance.save()
			question_author = get_object_or_404(
				User, username=question_instance.author)
			answer_author = get_object_or_404(User, username=parent.answer_author)
			Notification.objects.create_reply_notification(answer_author, reply)
			return HttpResponseRedirect(parent.question.get_absolute_url())


def delete_question(request, thread_id):
	try:
		thread_id = int(thread_id)
	except ValueError:
		raise Http404()
	username = request.user.username
	question_requested = get_object_or_404(Question, pk=thread_id)
	author = question_requested.author
	if author == username:
		question_requested.delete()
		Answer.objects.filter(question=thread_id).delete()
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
	question_requested = get_object_or_404(Question, pk=thread_id)
	answer_requested = Answer.objects.get(id=answer_id)
	author = answer_requested.answer_author
	if author == username:
		answer_requested.delete()
		question_requested.answers = Answer.objects.filter(
			question=thread_id).count()
		question_requested.save()
		return HttpResponseRedirect(question_requested.get_absolute_url())
	else:
		return HttpResponseRedirect(reverse('home'))


def edit_answer(request, thread_id, answer_id):
	try:
		thread_id = int(thread_id)
		answer_id = int(answer_id)
	except ValueError:
		raise Http404()
	answer_requested = get_object_or_404(Answer, pk=answer_id)
	author = answer_requested.answer_author
	if author == request.user.username:
		description = answer_requested.description
		data = {'description': description}
		prefilled_form = answer_form(data)
		return render(
			request,
			'thread_templates/edit.html',
			{
				'username': request.user.username,
				'form': prefilled_form,
				'thread_id': thread_id,
				'answer_id': answer_id
			})
	else:
		return HttpResponseRedirect(reverse('home'))


def edit_answer_submit(request, thread_id, answer_id):
	try:
		thread_id = int(thread_id)
		answer_id = int(answer_id)
	except ValueError:
		raise Http404()
	if request.method == 'POST' and request.POST:
		answer_requested = get_object_or_404(Answer, pk=answer_id)
		edited_answer = answer_form(request.POST)
		if edited_answer.is_valid():
			updated_answer = edited_answer.save(commit=False)
			answer_requested.description = updated_answer.description
			answer_requested.set_edited_time()
			answer_requested.save()
		return HttpResponseRedirect(answer_requested.question.get_absolute_url())
	else:
		return HttpResponseRedirect(reverse('home'))


def mark_answer_solved(request, thread_id):
	try:
		thread_id = int(thread_id)
	except ValueError:
		raise Http404()
	username = request.user.username
	question_requested = get_object_or_404(Question, pk=thread_id)
	author = question_requested.author
	if author == username:
		question_requested.solved = True
		question_requested.save()
		return HttpResponseRedirect(question_requested.get_absolute_url())
	else:
		return HttpResponseRedirect(reverse('home'))
