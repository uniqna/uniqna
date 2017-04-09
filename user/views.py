from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from ask.models import question
from threads.models import answer
from itertools import chain
from home.forms import editForm, changePasswordForm, emailForm
from random import randint
from django.core.mail import EmailMessage
from user.models import Notifications
from django.core.exceptions import ObjectDoesNotExist
import markdown2
# Create your views here.


def UserPage(request, usr):
    if usr == "anon":
        return render(request, "user_templates/userpage.html")
    requested_user = get_object_or_404(User, username=usr)
    user_questions = question.objects.filter(author=usr)
    user_answers = answer.objects.filter(answer_author=usr)
    for x in user_answers:
        x.description = markdown2.markdown(x.description, extras=["tables", "cuddled-lists"])
    for x in user_questions:
        x.description = markdown2.markdown(x.description, extras=["tables", "cuddled-lists"])
    # Combining questions and answers
    all_list = sorted(list(chain(user_questions, user_answers)), key=lambda instance: instance.created_time)
    return render(request, "user_templates/newuserpage.html",
                  {"user_instance": requested_user,
                   "questions": user_questions,
                   "answers": user_answers,
                   "allqa": all_list[::-1],
                   })


def EditProfile(request, usr):
    if request.method == "POST" and request.POST:
        print("inside post")
        requested_user = get_object_or_404(User, username=usr)
        profile_form = editForm(request.POST)
        if profile_form.is_valid():
            print("inside valid")
            requested_user.email = profile_form.cleaned_data["email"]
            requested_user.save()
            requested_user.student.bio = profile_form.cleaned_data["bio"]
            requested_user.student.university = profile_form.cleaned_data["university"]
            requested_user.student.course = profile_form.cleaned_data["course"]
            requested_user.student.school = profile_form.cleaned_data["school"]
            requested_user.student.grad_year = profile_form.cleaned_data["grad_year"]
            requested_user.student.save()
            print("saved")
            return HttpResponseRedirect("/user/" + requested_user.username)
        else:
            print("inside not valid")
    else:
        if usr == "anon":
            return render(request, "user_templates/userpage.html")
        requested_user = get_object_or_404(User, username=usr)
        data = {
            "email": requested_user.email,
            "bio": requested_user.student.bio,
            "university": requested_user.student.university,
            "course": requested_user.student.course,
            "school": requested_user.student.school,
            "grad_year": requested_user.student.grad_year,
        }
        profile_form = editForm(data)
        return render(request, "user_templates/newedit.html", {"regform": profile_form})


def ChangePassword(request, usr):
    req_user = get_object_or_404(User, username=usr)
    if request.method == "POST" and request.POST:
        cp_form = changePasswordForm(request.POST)
        if cp_form.is_valid():
            cur_pass = cp_form.cleaned_data["current_password"]
            a_user = authenticate(username=req_user.username, password=cur_pass)
            if a_user is not None:
                a_user.set_password(cp_form.cleaned_data["password"])
                a_user.save()
                login(request, a_user)
                return render(request, "user_templates/changepassword.html", {"user_instance": req_user, "success": 1})
            else:
                return render(request, "user_templates/newchangepassword.html", {"user_instance": req_user, "changeform": cp_form, "failed": 1})
        else:
            return render(request, "user_templates/newchangepassword.html", {"user_instance": req_user, "changeform": cp_form})

    else:
        cp_form = changePasswordForm()
        return render(request, "user_templates/newchangepassword.html", {"changeform": cp_form, "user_instance": req_user})


def forgot_password_view(request):
    if request.method == "POST" and request.POST:
        emf = emailForm(request.POST)
        if emf.is_valid():
            email = emf.cleaned_data["email"]
            print("badumtss")
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, "user_templates/newforgotpassword.html", {"emailform": emf, "notexist": 1})
            # Generating all the lowercase and uppercase chars
            chars = [chr(i) for i in range(65, 123)]
            # Randomising the length of the password
            length = randint(6, 8)
            # Choosing the password
            pwd = [chars[randint(0, len(chars))] for i in range(0, length)]
            # Generated password
            pwdstring = ''.join(pwd)
            # Make the password as the users password
            user.set_password(pwdstring)
            user.save()
            # Mail the random password
            body = "Hey " + str(user.username) + ", your new password is\n\n\n" + pwdstring + "\n\n\nGo here and login with your new password: www.uniqna.com\nAnd make sure to change your password to a more secure one."
            email_user = EmailMessage("Reset your password - uniqna.com", body, to=[email])
            if email_user.send():
                print("Success.")
                return render(request, "user_templates/newforgotpassword.html", {"success": 1})
        else:
            return render(request, "user_templates/newforgotpassword.html", {"emailform": emf})
    else:
        emf = emailForm()
        return render(request, "user_templates/newforgotpassword.html", {"emailform": emf})


def update_all(request):
    # Code for adding notification objects to all users
    # Delete after running it once
    us = User.objects.all()
    log = ""
    cnt = 0
    for u in us:
        try:
            print(u.notifications)
            print(u.username)
        except ObjectDoesNotExist:
            n = Notifications()
            n.user = u
            n.save()
            del n
            log += "<br>-> " + u.username
            cnt += 1
            log += "<br>==== " + str(cnt) + " users updated ==="
            return HttpResponse("<html>" + log + "</html>")
