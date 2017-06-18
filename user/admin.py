from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from user.models import student, Notification


class StudentInline(admin.StackedInline):
    model = student
    can_delete = False
    verbose_name_plural = 'Students'


class NotificationInline(admin.StackedInline):
    model = Notification
    can_delete = False
    verbose_name_plural = 'Notifications'


class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline, NotificationInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
