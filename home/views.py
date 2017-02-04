from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import get_template
from django.template import Template, Context
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ask.models import question
from user.models import student
from home.forms import registration
from threads.models import answer

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
        question.objects.PopUpdate()
        question_list = question.objects.order_by("-popularity")
        no_of_questions = question.objects.all().count()
        no_of_answers = answer.objects.all().count()
        no_of_solved = question.objects.filter(solved=True).count()
        no_of_solved_percentage = round((no_of_solved / no_of_questions) * 100)
        return render(request,
                      'home_templates/home.html',
                      {'username': username,
                       'question_list': question_list,
                       'no_of_questions': no_of_questions,
                       'no_of_answers': no_of_answers,
                       'no_of_solved_percentage': no_of_solved_percentage})
    else:
        return render(request,
                      'login_templates/login.html',
                      {'error': error})


def register(request):
    if request.method == 'POST':
        reg_form = registration(request.POST)
        if reg_form.is_valid():
            cd = reg_form.cleaned_data
            new_user = User.objects.create_user(username=cd["username"], email=cd["email"], password=cd["password"])
            new_profile = student(bio=cd["bio"], location=cd["location"], age=cd["age"], course=cd["course"], school=cd["school"], grad_year=cd["grad_year"])
            new_profile.user = new_user
            new_profile.save()
            login(request, new_user)
            return render(request,
                          'login_templates/welcome.html',
                          {'username': new_user.username})
        else:
            errors = []
            return render(request,
                          'login_templates/register.html',
                          {
                              'regform': reg_form,
                              'errors': reg_form.errors})
    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        reg_form = registration()
        return render(request,
                      'login_templates/register.html',
                      {'regform': reg_form})


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
        question_instance.save()
    return redirect('home')
