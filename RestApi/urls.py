from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from RestApi import views
app_name = "api"

urlpatterns = [
	url(r'answers/$', views.VotesView.as_view(), name="answers"),
	url(r'answers/(?P<pk>\d{1,3})/(?P<ud>[ud])/$', views.GetVote.as_view(), name="vote"),
]
