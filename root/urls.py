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
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.sitemaps import ThreadsSitemap

from root import settings
from home import views

sitemaps = {
	'thread': ThreadsSitemap()
}

urlpatterns = [
	url(r'^$', views.home, name="home"),
	url(r'^admin/', admin.site.urls),
	url(r'^(?P<tab>(qna|nsy|disc))/$', views.home, name="tab"),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^register/$', views.register, name='register'),
	url(r'^notifications/$', views.notifications_view, name='notifications'),
	url(r'^channel/(\w+)/$', views.channel_view, name='channel'),
	url(r'^notification/(\d+)/$', views.notification_redirect, name='notif'),
	url(r'^new/', include('post.urls')),
	url(r'^thread/', include('threads.urls')),
	url(r'^user/', include('user.urls')),
	url(r'^api/', include('api.urls')),
	url(r'^search/', include('search.urls')),
	url(r'^user/', include('user.urls')),
	url(r'^sitemap\.xml$', sitemap, {
		'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
	url(r'^robots.txt', include('robots.urls')),
	url(r'^test-email/$', views.test_email_templates)
]

if settings.DEBUG is True:
	urlpatterns += staticfiles_urlpatterns()
