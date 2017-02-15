from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from user.models import student, Notifications


class StudentInline(admin.StackedInline):
    model = student
    can_delete = False
    verbose_name_plural = 'Students'


class NotificationsInline(admin.StackedInline):
    model = Notifications
    can_delete = False
    verbose_name_plural = 'Notifications'


class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline, NotificationsInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
