from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import get_template
from django.template import RequestContext
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ask.models import question, tag
from user.models import student, Notifications, Answered
from home.forms import registration
from threads.models import answer

token = False  # An error token - True when it encounters invalid credentials.


def validation(request):
    if request.method == 'POST' and request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return render(request, "login_templates/login.html", {"failed": 1})
    else:
        return HttpResponseRedirect(reverse('home'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def home(request, tab="home"):
    if request.method == 'GET':
        if request.user.is_authenticated:
            username = request.user.username
            question.objects.PopUpdate()
            if tab == "home":
                question_list = question.objects.order_by("-hot")
            if tab == "qna":
                question_list = question.objects.filter(metatype="question").order_by("-hot")
            if tab == "nsy":
                question_list = question.objects.filter(metatype="question", solved=False).order_by("-hot")
            if tab == "disc":
                question_list = question.objects.filter(metatype="discussion").order_by("-hot")
            no_of_questions = question.objects.filter(metatype="question").count()
            no_of_answers = answer.objects.filter(metatype="question").count()
            no_of_solved = question.objects.filter(metatype="question", solved=True).count()
            if not no_of_questions:
                no_of_solved_percentage
            else:
                no_of_solved_percentage = round((no_of_solved / no_of_questions) * 100)
            return render(request,
                          'home_templates/newhome.html',
                          {'tab': tab,
                           'question_list': question_list,
                           'no_of_questions': no_of_questions,
                           'no_of_answers': no_of_answers,
                           'no_of_solved_percentage': no_of_solved_percentage})
        else:
            question_list = question.objects.all().order_by("-hot")[:3]
            return render(request,
                          'login_templates/login.html',
                          {'tab': tab,
                           'question_list': question_list, })

    if request.method == 'POST' and request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            question_list = question.objects.all().order_by("-hot")[:3]
            return render(request, "login_templates/login.html", {"failed": 1,
                                                                  'question_list': question_list,
                                                                  })


def register(request):
    if request.method == 'POST':
        reg_form = registration(request.POST)
        if reg_form.is_valid():
            cd = reg_form.cleaned_data
            new_user = User.objects.create_user(username=cd["username"], email=cd["email"], password=cd["password"])
            new_profile = student(bio=cd["bio"], university=cd["university"], course=cd["course"], school=cd["school"], grad_year=cd["grad_year"])
            new_profile.user = new_user
            new_profile.unique_username = cd["username"].lower()
            new_profile.save()
            notif = Notifications()
            notif.user = new_user
            notif.save()
            login(request, new_user)
            return HttpResponseRedirect(reverse('home'))
        else:
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


def tag_view(request, tagname):
    try:
        tagname = str(tagname)
    except ValueError:
        raise Http404()
    if request.user.is_authenticated:
        tag_instance = get_object_or_404(tag, name=tagname)
        return render(request, "tag_templates/tags.html", {'tags': tag_instance})
    else:
        return HttpResponseRedirect(reverse('home'))


def notif_redirect(request, pk):
    ans_notif = get_object_or_404(Answered, pk=pk)
    ans_notif.read = True
    ans_notif.save()
    ques = ans_notif.theanswer.question.id
    ans = ans_notif.theanswer.id
    return HttpResponseRedirect("/thread/" + str(ques) + "/#a" + str(ans))
