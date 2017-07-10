from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views


urlpatterns = [
    url(r'answers/$', views.VotesView.as_view(), name="answers"),
    url(r'frontpage/$', views.FrontPage.as_view(), name="frontpage"),
    url(r'answers/(?P<pk>\d{1,3})/(?P<ud>[ud])/$', views.AnswerVote.as_view(), name="answer_vote"),
    url(r'questions/(?P<pk>\d{1,3})/(?P<ud>[ud])/$', views.QuestionVote.as_view(), name="question_vote"),
    url(r'create/channel$', views.CreateChannel.as_view(), name="CreateChannel"),
    url(r'suggest/$', views.SuggestChannel.as_view(), name="SuggestChannel"),
    url(r'channels/$', views.GetChannels.as_view(), name="GetChannels"),
    url(r'availability/$', views.CheckUsername.as_view(), name="availability"),
]
