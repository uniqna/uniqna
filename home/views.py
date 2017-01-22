from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import get_template
from django.template import Template, Context
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ask.models import question
from .forms import registration
from root.algorithms import popularity
token = False  # An error token - True when it encounters invalid credentials.


def validation(request):
    global token
    if request.method == 'POST' and request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            token = True
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('home'))


def logout_view(request):
    global token
    logout(request)
    token = False
    return HttpResponseRedirect(reverse('home'))


def home(request):
    global token
    error = token  # Transferring the token's boolean and resetting token.
    token = False
    if request.user.is_authenticated:
        username = request.user.username
        question_list = question.objects.order_by("-popularity")
        return render(request,
                      'home_templates/home.html',
                      {'username': username,
                       'question_list': question_list})
    else:
        return render(request,
                      'login_templates/login.html',
                      {'error': error})


def register(request):
    if request.method == 'POST':
        submitted_form = registration(request.POST)
        if submitted_form.is_valid():
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            new_user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password)
            login(request, new_user)
            return render(request,
                          'login_templates/welcome.html',
                          {'username': username})
        else:
            errors = []
            for key in submitted_form.errors:
                errors.append(submitted_form.errors.get(key))
            unsubmitted_form = registration()
            return render(request,
                          'login_templates/register.html',
                          {'form': unsubmitted_form,
                           'errors': errors})
    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        unsubmitted_form = registration()
        return render(request,
                      'login_templates/register.html',
                      {'form': unsubmitted_form})


def welcome(request):
    return render(request,
                  'login_templates/welcome.html',
                  {'username': username})


def vote(request, qid, upordown):
    try:
        qid = int(qid)
    except ValueError:
        raise Http404()
    if request.user.is_authenticated:
        question_instance = get_object_or_404(question, pk=qid)
        if upordown == 'u':
            vote_on = question_instance.ups
            vote_on_other = question_instance.downs
        elif upordown == 'd':
            vote_on = question_instance.downs
            vote_on_other = question_instance.ups
        if request.user not in vote_on.all():
            vote_on.add(request.user)
            vote_on_other.remove(request.user)
        else:
            vote_on.remove(request.user)
        upvotes = question_instance.ups.count()
        downvotes = question_instance.downs.count()
        question_instance.points = upvotes - downvotes
        question_instance.popularity = popularity.popularity(question_instance)
        question_instance.save()
    return redirect('home')
