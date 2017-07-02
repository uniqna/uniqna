from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import markdown2

from post.models import Question
from post.forms import post_form
from threads.forms import reply_form
from threads.models import Answer
from user.models import Notification


def thread(request, thread_id, slug="", answer_id=""):
	try:
		thread_id = int(thread_id)
	except ValueError:
		raise Http404()
	post_requested = get_object_or_404(Question, pk=thread_id)
	description = markdown2.markdown(
		post_requested.description,
		extras=["tables", "cuddled-lists"]
	)
	unsubmitted_reply = reply_form()
	Answer._tree_manager.rebuild()  # You rebuild the tree and then query.
	all_replies = Answer.objects.filter(
		question=post_requested).order_by('tree_id', 'lft')
	replies_count = all_replies.count()
	data = {'description': post_requested.description}
	edit_form = post_form(data)
	for x in all_replies:
		x.description = markdown2.markdown(
			x.description, extras=["tables", "cuddled-lists"])
	return render(
		request,
		'thread.html',
		{
			'post': post_requested,
			'description': description,
			'form': unsubmitted_reply,
			'nodes': all_replies,
			'replies': replies_count,
			'edit_form': edit_form
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
	return render(request, 'thread.html', {
		'post': parent_ques,
		'nodes': replies,
		'description': description,
		'reply': True
	})


def submit_answer(request, thread_id):
	if request.method == 'POST' and request.POST:
		question_answered = get_object_or_404(Question, pk=thread_id)
		question_metatype = question_answered.metatype
		submitted_answer = reply_form(request.POST)
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
			if not request.user == question_author:
				Notification.objects.create_answer_notification(
					question_author, instance)
			return HttpResponseRedirect(question_answered.get_absolute_url())


def submit_reply(request, answer_id):
	if request.method == "POST" and request.POST:
		parent = Answer.objects.filter(
			pk=answer_id).select_related('question')[0]
		question_instance = parent.question
		question_id = question_instance.pk
		submitted_reply = reply_form(request.POST)
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
			answer_author = get_object_or_404(User, username=parent.answer_author)
			if not request.user == answer_author:
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
	reply_requested = get_object_or_404(Answer, pk=answer_id)
	author = reply_requested.answer_author
	if author == request.user.username or request.user.is_superuser:
		description = reply_requested.description
		data = {'description': description}
		prefilled_form = reply_form(data)
		return render(
			request,
			'edit_reply.html',
			{
				'username': request.user.username,
				'form': prefilled_form,
				'thread_id': thread_id,
				'reply': reply_requested
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
		edited_answer = reply_form(request.POST)
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
