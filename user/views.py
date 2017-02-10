from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib.auth.models import User
from ask.models import question
from threads.models import answer
from itertools import chain
from home.forms import registration
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
    if usr == "anon":
        return render(request, "user_templates/userpage.html")
    requested_user = get_object_or_404(User, username=usr)
    data = {
        "username": requested_user.username,
        "email": requested_user.email,
        "bio": requested_user.student.bio,
        "university": requested_user.student.university,
        "course": requested_user.student.course,
        "school": requested_user.student.school,
        "grad_year": requested_user.student.grad_year,
    }
    profile_form = registration(data)
    return render(request, "edit_profile_templates/edit.html", {"regform": profile_form})
