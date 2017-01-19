from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import get_template
from django.template import Template, Context
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ask.models import question
from .forms import registration, loginForm

token = False  # An error token - True when it encounters invalid credentials.


def validation(request):
    global token
    if request.method == 'POST' and request.POST:
        lform = loginForm(request.POST)
        if lform.is_valid():
            username = lform.cleaned_data['username']
            password = lform.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                return render(request, "login_templates/login.html", {
                    "form": lform,
                    "failed": 1
                })
    else:
        lform = loginForm()
        return render(request, "login_templates/login.html", {"form": lform})


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
        question_list = question.objects.all()
        return render(request,
                      'home_templates/home.html',
                      {'question_list': question_list})
    else:
        return render(request,
                      'home_templates/home.html')


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
