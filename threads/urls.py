from django.conf.urls import url
from threads import views

urlpatterns = [
    url(r'(\d{1,5})/$', views.thread, name='thread'),
    url(r'(\d{1,5})/answer/$', views.submit_answer),
    url(r'(\d{1,5})/delete/$', views.delete_question, name='delete_question'),
    url(r'(\d{1,5})/delete/answer/(\d{1,5})$', views.delete_answer, name='delete_answer'),
    url(r'(\d{1,5})/edit/answer/(\d{1,5})$', views.edit_answer, name='edit_answer'),
    url(r'(\d{1,5})/edit/answer/(\d{1,5})/submit/$', views.edit_answer_submit, name='edit_answer_submit'),
    url(r'(\d{1,5})/answer/(\d{1,5})/([up,down])/$', views.vote, name='vote'),
]
