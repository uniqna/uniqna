from django.conf.urls import url

from post import views

urlpatterns = [
    url(r'^ask$', views.ask, name='ask'),
    url(r'^discuss$', views.discuss, name='discuss'),
    url(r'^submit/(?P<metatype>(discussion|question))',
        views.submit, name="submit"),
]
