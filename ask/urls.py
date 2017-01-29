from django.conf.urls import url
from ask import views

urlpatterns = [
    url(r'^$', views.ask),
    url(r'^submit/$', views.submit),
]
