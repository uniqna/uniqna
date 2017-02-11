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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url, include
from django.contrib import admin
from home import views
from tinymce import urls
from threads import urls
from user import urls
from RestApi import urls
from root import settings
from search import urls
from user.views import forgot_password_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name="home"),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^tag/(\w+)/$', views.tag_view, name='tags'),
    url(r'^notification/(\d+)/$', views.notif_redirect, name='notif'),
    url(r'^ask/', include('ask.urls')),
    url(r'^thread/', include('threads.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^api/', include('RestApi.urls')),
    url(r'^search', include('search.urls')),
    url(r'^forgotpassword/$', forgot_password_view, name="forgot"),
]

if settings.DEBUG is True:
    urlpatterns += staticfiles_urlpatterns()
