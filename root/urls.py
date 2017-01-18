"""root URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from home import views
from userapp.views import UserPage
from tinymce import urls
from threads import urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^validation/$', views.validation),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register),
    url(r'^ask/', include('ask.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^thread/', include('threads.urls')),
    url(r'^user/(?P<usr>[a-zA-Z_.]+)/$', UserPage, name="user"),
]
