from django.conf.urls import url
from threads import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'(\d{1,5})/$', views.thread, name='thread'),
   # url(r'api/$', views.VotesView.as_view()),
   # url(r'^api/(?P<pk>[0-9]+)$', views.vote_rest),
    url(r'(\d{1,5})/answer/$', views.submit_answer),
    url(r'(\d{1,5})/delete/$', views.delete_question, name='delete_question'),
    url(r'(\d{1,5})/solved/$', views.mark_answer_solved, name='mark_answer_solved'),
    url(r'(\d{1,5})/delete/answer/(\d{1,5})$', views.delete_answer, name='delete_answer'),
    url(r'(\d{1,5})/edit/answer/(\d{1,5})$', views.edit_answer, name='edit_answer'),
    url(r'(\d{1,5})/edit/answer/(\d{1,5})/submit/$', views.edit_answer_submit, name='edit_answer_submit'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
