from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from random import randint

from post.forms import post_form
from post.models import Channel
from user.models import student


def ask(request):
	if request.user.is_authenticated:
		metatype = "question"
		unsubmitted_form = post_form()
		return render(
			request,
			'new.html',
			{
				'metatype': metatype,
				'channels': Channel.objects.all(),
				'form': unsubmitted_form
			})
	else:
		return HttpResponseRedirect(reverse('home'))


def discuss(request):
	if request.user.is_authenticated:
		metatype = "discussion"
		unsubmitted_form = post_form()
		return render(
			request,
			'new.html',
			{
				'metatype': metatype,
				'channels': Channel.objects.all(),
				'form': unsubmitted_form
			})
	else:
		return HttpResponseRedirect(reverse('home'))


def submit(request, metatype):
	if request.method == 'POST' and request.POST and request.user.is_authenticated:
		submitted_form = post_form(request.POST)
		if submitted_form.is_valid():
			instance = submitted_form.save(commit=False)
			instance.author = request.user.username
			instance.metatype = metatype
			instance.save()
			instance.ups.add(request.user)
			if request.POST['channels']:
				selected_channels = request.POST['channels']
				channel_list = selected_channels.split(",")
				channel_list = [x.lower() for x in channel_list if x != '']
				for channel in channel_list:
					this_channel = Channel.objects.get(name=channel)
					instance.channels.add(this_channel)
			return HttpResponseRedirect(instance.get_absolute_url())
		else:
			return render(
				request,
				"post_templates/new.html",
				{
					"username": request.user.username,
					"tags": Channel.objects.all(),
					"form": submitted_form,
					"errors": submitted_form.errors
				})
	else:
		return HttpResponseRedirect(reverse('home'))


def random(request):
	if request.user.is_superuser:
		metatype = "question"
		unsubmitted_form = post_form()
		return render(
			request,
			'random_user_new.html',
			{
				'metatype': metatype,
				'channels': Channel.objects.all(),
				'form': unsubmitted_form
			}
		)
	else:
		return HttpResponseRedirect(reverse('home'))


def random_submit(request):
	if request.method == 'POST' and request.POST and request.user.is_superuser:
		submitted_form = post_form(request.POST)
		if submitted_form.is_valid():

			username = request.POST["username"]
			bio = request.POST["bio"]
			email = username + "@testing.com"
			chars = [chr(i) for i in range(65, 123)]
			pwd = [chars[randint(0, len(chars) - 1)] for i in range(0, 10)]
			pwdstring = ''.join(pwd)
			new_user = User.objects.create_user(
				username=username,
				email=email,
				password=pwdstring
			)
			new_profile = student(bio=bio)
			new_profile.user = new_user
			new_profile.save()

			instance = submitted_form.save(commit=False)
			instance.author = username
			instance.metatype = "question"
			instance.save()
			instance.ups.add(request.user)
			if request.POST['selectedchannels']:
				selected_channels = request.POST['selectedchannels']
				channel_list = selected_channels.split(",")
				channel_list = [x.lower() for x in channel_list if x != '']
				for channel in channel_list:
					this_channel = Channel.objects.get(name=channel)
					instance.channels.add(this_channel)
			return HttpResponseRedirect("/thread/" + str(instance.pk))
		else:
			return render(
				request,
				"post_templates/random_user_new.html.html",
				{
					"username": request.user.username,
					"tags": Channel.objects.all(),
					"form": submitted_form,
					"errors": submitted_form.errors
				})
	else:
		return HttpResponseRedirect(reverse('home'))
