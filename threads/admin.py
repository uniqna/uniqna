from django.contrib import admin
from threads.models import answer
from mptt.admin import MPTTModelAdmin


class answer_admin(admin.ModelAdmin):
    list_display = ('id', 'question', 'description', 'answer_author',
                    'created_time', 'edited', 'edited_time', 'score')


admin.site.register(answer, MPTTModelAdmin)
