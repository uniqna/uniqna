from itertools import chain
from random import randint

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import markdown2

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

	for x in user_replies:
		x.description = markdown2.markdown(
			x.description,
			extras=["tables", "cuddled-lists"])

	for x in user_posts:
		x.description = markdown2.markdown(
			x.description,
			extras=["tables", "cuddled-lists"])

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
	if request.method == "POST" and request.POST:
		requested_user = get_object_or_404(User, username=user)
		profile_form = editForm(request.POST)
		if profile_form.is_valid():
			requested_user.email = profile_form.cleaned_data["email"]
			requested_user.save()
			requested_user.student.bio = profile_form.cleaned_data["bio"]
			requested_user.student.university = profile_form.cleaned_data["university"]
			requested_user.student.course = profile_form.cleaned_data["course"]
			requested_user.student.school = profile_form.cleaned_data["school"]
			requested_user.student.grad_year = profile_form.cleaned_data["grad_year"]
			requested_user.student.save()
			return HttpResponseRedirect("/user/" + requested_user.username)
		else:
			return render(
				request,
				"user_manage.html",
				{"regform": profile_form, "error": True}
			)

	else:
		requested_user = get_object_or_404(User, username=user)
		data = {
			"email": requested_user.email,
			"bio": requested_user.student.bio,
			"university": requested_user.student.university,
			"course": requested_user.student.course,
			"school": requested_user.student.school,
			"grad_year": requested_user.student.grad_year,
		}
		profile_form = editForm(data)
		return render(
			request,
			"user_manage.html",
			{"regForm": profile_form}
		)


def change_password(request, user):
	req_user = get_object_or_404(User, username=user)

	# Don't render page if the user isn't asking for
	# his own change password page
	if not req_user == request.user:
		return HttpResponseRedirect(reverse(
			'user',
			kwargs={"user": user}
		))

	if request.method == "POST" and request.POST:
		cp_form = changePasswordForm(request.POST)

		if cp_form.is_valid():
			cur_pass = cp_form.cleaned_data["current_password"]
			a_user = authenticate(username=req_user.username, password=cur_pass)

			if a_user is not None:
				a_user.set_password(cp_form.cleaned_data["password"])
				a_user.save()
				login(request, a_user)
				return render(
					request,
					"user_templates/changepassword.html",
					{
						"user_instance": req_user,
						"success": 1
					})
			else:
				return render(
					request,
					"user_templates/changepassword.html",
					{
						"user_instance": req_user,
						"changeform": cp_form,
						"failed": 1
					})
		else:
			return render(
				request,
				"user_templates/changepassword.html",
				{
					"user_instance": req_user,
					"changeform": cp_form
				})

	else:
		cp_form = changePasswordForm()
		return render(
			request,
			"user_templates/changepassword.html",
			{
				"changeform": cp_form,
				"user_instance": req_user
			})


def forgot(request):
	navtext = "Forgot Password?"
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
		mail_html = render_email("forgot_password.html", {"password": pwdstring})
		opts = {
			"recipents": user.email,
			"subject": "Recover your account - uniqna",
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
		# Javascript true
		toggle = toggle[0].upper() + toggle[1:]
		this_student = get_object_or_404(student, user=request.user)
		this_student.notification_emails = toggle
		this_student.save()
		return HttpResponse(toggle)
	else:
		return Http404()
