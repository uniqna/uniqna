from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib.auth.models import User
from ask.models import question
from threads.models import answer
# Create your views here.


def UserPage(request, usr):
    if usr == "anon":
        return render(request, "userapp/userpage.html")
    requested_user = get_object_or_404(User, username=usr)
    user_questions = question.objects.filter(author=usr)
    user_answers = answer.objects.filter(answer_author=usr)

    return render(request, "userapp/userpage.html", {
        "user_instance": requested_user,
        "questions": user_questions,
        "answers": user_answers
        })
