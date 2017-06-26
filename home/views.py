from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from home.forms import registration
from post.models import Channel, Question
from root.email import render_email, send_email
from threads.models import Answer
from user.models import student, Notification


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))


def home(request, tab="home"):
	if request.method == 'GET':
		if request.user.is_authenticated:
			username = request.user.username
			Question.objects.popularity_update()
			if tab == "home":
				question_list = Question.objects.order_by("-hot")
			elif tab == "questions":
				question_list = Question.objects.filter(
					metatype="question").order_by("-hot")
			elif tab == "unsolved":
				question_list = Question.objects.filter(
					metatype="question", solved=False).order_by("-hot")
			elif tab == "discussions":
				question_list = Question.objects.filter(
					metatype="discussion").order_by("-hot")
			no_of_questions = Question.objects.filter(
				metatype="question").count()
			no_of_answers = Answer.objects.filter(metatype="question").count()
			no_of_solved = Question.objects.filter(
				metatype="question", solved=True).count()
			no_of_solved_percentage = round(
				(no_of_solved / 1) * 100)
			return render(
				request,
				'home.html',
				{
					'tab': tab,
					'question_list': question_list,
					'no_of_questions': no_of_questions,
					'no_of_answers': no_of_answers,
					'no_of_solved_percentage': no_of_solved_percentage
				})
		else:
			question_list = Question.objects.all().order_by("-hot")[:3]
			return render(
				request,
				'login.html',
				{'tab': tab,
					'question_list': question_list, })

	if request.method == 'POST' and request.POST:
		username = request.POST['username']
		password = request.POST['password']
		try:
			user = User._default_manager.get(username__iexact=username)
			user_auth = authenticate(username=user.username, password=password)
		except User.DoesNotExist:
			user_auth = None
		if user_auth is not None:
			login(request, user_auth)
			return HttpResponseRedirect(reverse('home'))
		else:
			question_list = Question.objects.all().order_by("-hot")[:3]
			return render(request, "login.html", {
				"failed": True,
				"question_list": question_list,
			})


def register(request):
	navtext = "Register!"
	if request.method == 'POST' and request.POST:
		reg_form = registration(request.POST)
		if reg_form.is_valid():
			cd = reg_form.cleaned_data
			new_user = User.objects.create_user(
				username=cd["username"],
				email=cd["email"],
				password=cd["password"])
			new_profile = student(
				bio=cd["bio"],)
			new_profile.user = new_user
			new_profile.save()
			login(request, new_user)
			mail_html = render_email("welcome_email.html", {"username": new_user.username})
			opts = {
				"recipents": new_user.email,
				"subject": "Welcome aboard.",
				"body": mail_html
			}
			send_email(opts)
			return HttpResponseRedirect(reverse('home'))
		else:
			return render(
				request,
				'register.html',
				{
					'regform': reg_form,
					'navtext': navtext
				})

	elif request.user.is_authenticated:
		return HttpResponseRedirect(reverse('home'))
	else:
		reg_form = registration()
		return render(
			request,
			'register.html',
			{'regform': reg_form, 'navtext': navtext})


def channel_view(request, channel_name):
	try:
		channel_name = str(channel_name)
	except ValueError:
		raise Http404()
	if request.user.is_authenticated:
		channel_instance = get_object_or_404(Channel, name=channel_name)
		return render(
			request,
			"channel.html",
			{'channel': channel_instance})
	else:
		return HttpResponseRedirect(reverse('home'))


def notifications_view(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('home'))
	else:
		return render(request, "notifications.html")


def notification_redirect(request, pk):
	notif = get_object_or_404(Notification, pk=pk)
	if request.user != notif.user:
		raise Http404()
	if not notif.read:
		notif.read = True
		notif.save()
	# the answer object
	answer_instance = get_object_or_404(Answer, pk=notif.object_id)
	url = answer_instance.get_absolute_url()
	return HttpResponseRedirect(url)


def test_email_templates(request):
	return render(request, "email_templates/welcome_email.html")
