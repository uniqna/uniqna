from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import get_template
from django.template import Template, Context
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .forms import registration

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
        return render(request,
                      'home_templates/home.html',
                      {'username': username})
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
