from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.postgres.search import SearchVector

from post.models import Question


def search(request):
	if request.method == 'GET' and request.GET:
		submitted_query = request.GET['query']
		if submitted_query.strip() == "":
			return HttpResponseRedirect(request.META["HTTP_REFERER"])
		filtered_questions = Question.objects.annotate(search=SearchVector('title', 'description'), ).filter(search=submitted_query)
		return render(
			request,
			'results.html',
			{
				'query': submitted_query,
				'results': filtered_questions,
			})
