from django.conf.urls import url
from ask import views

urlpatterns = [
    url(r'^$', views.ask, name='ask'),
    url(r'^submit/$', views.submit, name="question_submit"),
]
