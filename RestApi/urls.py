from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from RestApi import views


urlpatterns = [
	url(r'answers/$', views.VotesView.as_view(), name="answers"),
	url(r'answers/(?P<pk>\d{1,3})/(?P<ud>[ud])/$', views.AnswerVote.as_view(), name="answer_vote"),
	url(r'questions/(?P<pk>\d{1,3})/(?P<ud>[ud])/$', views.QuestionVote.as_view(), name="question_vote"),
	url(r'createtag/$', views.CreateTag.as_view(), name="CreateTag"),
	url(r'test/$', views.TestView, name="test"),
	url(r'testpost/$', views.TestPost.as_view(), name="testpost"),
	url(r'suggest/$', views.SuggestTag.as_view(), name="SuggestTag"),
]
