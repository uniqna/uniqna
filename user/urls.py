from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^(?P<usr>[a-zA-Z_.]+)/$', views.UserPage, name="user"),
]
