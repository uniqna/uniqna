from django.conf.urls import url
from threads import views

urlpatterns = [
    url(r'(\d{1,5})$', views.thread),
]
