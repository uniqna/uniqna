from django.contrib import admin
from threads.models import answer

# Register your models here.


class answer_admin(admin.ModelAdmin):
    list_display = ('id', 'question', 'description', 'answer_author', 'created_time', 'edited', 'edited_time')

admin.site.register(answer, answer_admin)
