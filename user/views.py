from itertools import chain
from random import randint

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse

from root.algorithms.parser import parse

from home.forms import editForm, changePasswordForm, emailForm
from post.models import Question
from root.email import render_email, send_email
from threads.models import Answer
from user.models import student


def user_page(request, user):
	if user == "anon":
		return render(request, "user_templates/userpage.html")

	requested_user = get_object_or_404(User, username=user)
	user_posts = Question.objects.filter(author=user)
	user_replies = Answer.objects.filter(answer_author=user)
	user_posts = parse(user_posts)
	user_replies = parse(user_replies)

	all_list = sorted(
		list(chain(user_posts, user_replies)),
		key=lambda instance: instance.created_time)
	post_score = sum([x.points for x in Question.objects.filter(
		author=requested_user.username) if x.points > 1])
	reply_score = sum([x.points for x in Answer.objects.filter(
		answer_author=requested_user.username) if x.points > 1])
	karma = round((post_score * 1.732) + reply_score)

	return render(
		request,
		"profile.html",
		{
			"user": requested_user,
			"posts": user_posts,
			"replies": user_replies,
			"all": all_list[::-1],
			"karma": karma,
		})


def edit_profile(request, user):
	requested_user = get_object_or_404(User, username=request.user)
	data = {"bio": requested_user.student.bio, }
	profile_form = editForm(data)
	password_form = changePasswordForm()
	if request.method == "POST" and request.POST:
		profile_form = editForm(request.POST)
		if request.POST.get('manage'):
			if profile_form.is_valid():
				requested_user.save()
				requested_user.student.bio = profile_form.cleaned_data["bio"]
				requested_user.student.save()
				return HttpResponseRedirect(reverse('user', kwargs={'user': user}))
			else:
				return render(
					request,
					"user_manage.html",
					{"edit_form": profile_form, "password_form": password_form}
				)
		elif request.POST.get('password'):
			submitted_form = changePasswordForm(request.POST)
			if submitted_form.is_valid():
				cd = submitted_form.cleaned_data
				cur_pass = cd["current_password"]
				a_user = authenticate(username=request.user.username, password=cur_pass)
				if a_user is not None:
					a_user.set_password(cd["new_password"])
					a_user.save()
					login(request, a_user)
					return HttpResponseRedirect(reverse('user', kwargs={'user': user}))
				else:
					return render(
						request,
						"user_manage.html",
						{"edit_form": profile_form, "password_form": password_form, "validation_failed": True}
					)
			else:
				return render(
					request,
					"user_manage.html",
					{"edit_form": profile_form, "password_form": submitted_form}
				)
	else:
		return render(
			request,
			"user_manage.html",
			{"edit_form": profile_form, "password_form": password_form}
		)


def forgot(request):
	navtext = "Forgot?"
	if request.method == "POST" and request.POST:
		email = request.POST['email']
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			return render(request, "forgot.html", {"notexist": True})
		chars = [chr(i) for i in range(65, 123)]
		length = randint(6, 8)
		pwd = [chars[randint(0, len(chars) - 1)] for i in range(0, length)]
		pwdstring = ''.join(pwd)
		user.set_password(pwdstring)
		user.save()
		mail_html = render_email("forgot.html", {"password": pwdstring, "user": user})
		opts = {
			"recipents": user.email,
			"subject": "Recover your account",
			"body": mail_html
		}
		send_email(opts)
		return render(
			request,
			"forgot.html",
			{"success": True, "navtext": navtext}
		)
	else:
		return render(
			request,
			"forgot.html",
			{"navtext": navtext}
		)


def toggle_email_notification(request, user):
	if request.method == "POST" and request.POST:
		if not request.user.username == user:
			return Http404()

		toggle = request.POST["toggle"]
		this_student = get_object_or_404(student, user=request.user)
		this_student.notification_emails = toggle
		this_student.save()
		return HttpResponse(toggle)
	else:
		return Http404()
