from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from ask.models import question
from threads.models import answer
from itertools import chain
from home.forms import editForm, changePasswordForm
# Create your views here.


def UserPage(request, usr):
    if usr == "anon":
        return render(request, "user_templates/userpage.html")
    requested_user = get_object_or_404(User, username=usr)
    user_questions = question.objects.filter(author=usr)
    user_answers = answer.objects.filter(answer_author=usr)
    # Combining questions and answers
    all_list = sorted(list(chain(user_questions, user_answers)), key=lambda instance: instance.created_time)
    return render(request, "user_templates/userpage.html",
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
        return render(request, "user_templates/edit.html", {"regform": profile_form})


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
                return render(request, "user_templates/changepassword.html", {"user_instance": req_user, "changeform": cp_form, "failed": 1})
        else:
            return render(request, "user_templates/changepassword.html", {"user_instance": req_user, "changeform": cp_form})

    else:
        cp_form = changePasswordForm()
        return render(request, "user_templates/changepassword.html", {"changeform": cp_form, "user_instance": req_user})
