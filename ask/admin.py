from django.contrib import admin
from ask.models import question

# Register your models here.


class question_admin(admin.ModelAdmin):
    list_display = ('id', 'title', 'answers', 'author', 'created_time', 'solved')

admin.site.register(question, question_admin)
