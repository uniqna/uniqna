from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from threads import views

"""
Weird bug in url.
Placing the submitreply url after the thread redirects
all the requests to the views.thread function instead
of views.submit_reply function. So I have moved the
reply url above the thread entry.

Update: I think I know the reason.
"""

urlpatterns = [
	url(r'(?P<thread_id>\d{1,5})/reply/(?P<answer_id>\d{1,5})/$', views.reply, name='reply'),
	url(r'reply/(?P<answer_id>\d{1,5})/$', views.submit_reply, name="submitreply"),
	url(r'(?P<thread_id>\d{1,5})-(?P<slug>[-\w\d]+)?$', views.thread, name='thread'),
	url(r'(?P<thread_id>\d{1,5})#a(?P<answer_id>\d{1,5})$', views.thread, name='answer'),
	url(r'(?P<thread_id>\d{1,5})/answer/$', views.submit_answer, name='submit_answer'),
	url(r'(?P<thread_id>\d{1,5})/delete/$', views.delete_question, name='delete_post'),
	url(r'(?P<thread_id>\d{1,5})/solved/$', views.mark_answer_solved, name='mark_answer_solved'),
	url(r'(?P<thread_id>\d{1,5})/delete/answer/(?P<answer_id>\d{1,5})$', views.delete_answer, name='delete_answer'),
	url(r'(?P<thread_id>\d{1,5})/edit/answer/(?P<answer_id>\d{1,5})$', views.edit_answer, name='edit_answer'),
	url(r'(?P<thread_id>\d{1,5})/edit/answer/(?P<answer_id>\d{1,5})/submit/$', views.edit_answer_submit, name='edit_answer_submit'),
	url(r'(?P<thread_id>\d{1,5})/(?P<slug>[-\w\d]+)?/?(#a\d{1,5})?$', views.thread, name="alt_thread"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
