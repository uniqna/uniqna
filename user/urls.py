from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^(?P<usr>[_a-zA-Z0-9]{3,15})/$', views.UserPage, name="user"),
]
