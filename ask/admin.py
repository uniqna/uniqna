from django.contrib import admin
from ask.models import question, tag

# Register your models here.


class question_admin(admin.ModelAdmin):
    list_display = ('id', 'title', 'answers', 'author', 'created_time', 'solved')
    filter_horizontal = ('ups',)

admin.site.register(question, question_admin)
admin.site.register(tag)
