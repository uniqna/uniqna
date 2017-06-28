from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^(?P<user>[_a-zA-Z0-9]{2,15})(/replies)?/$', views.user_page, name="user"),
    url(r'^(?P<user>[_a-zA-Z0-9]{2,15})/manage/$', views.edit_profile, name="edit_profile"),
    url(r'^(?P<user>[_a-zA-Z0-9]{2,15})/toggle-email/$', views.toggle_email_notification, name="toggle_email"),
]
