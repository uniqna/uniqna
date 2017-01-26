from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from user.models import student


class StudentInline(admin.StackedInline):
    model = student
    can_delete = False
    verbose_name_plural = 'student'


class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
