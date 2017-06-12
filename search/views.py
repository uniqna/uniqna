from django.shortcuts import render
from ask.models import Question
from threads.models import answer


def search(request):
    if request.method == 'GET' and request.GET:
        no_of_questions = Question.objects.all().count()
        no_of_answers = answer.objects.all().count()
        no_of_solved = Question.objects.filter(solved=True).count()
        no_of_solved_percentage = round((no_of_solved / no_of_questions) * 100)
        submitted_query = request.GET['query']
        filtered_questions = Question.objects.filter(
            title__search=submitted_query)
        return render(request,
                      'result_templates/results.html',
                      {'query': submitted_query,
                       'results': filtered_questions,
                       'username': request.user.username,
                       'no_of_questions': no_of_questions,
                       'no_of_answers': no_of_answers,
                       'no_of_solved_percentage': no_of_solved_percentage})
