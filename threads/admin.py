from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from threads.models import Answer


class answer_admin(admin.ModelAdmin):
    list_display = ('id', 'question', 'description', 'answer_author',
                    'created_time', 'edited', 'edited_time', 'score')


admin.site.register(Answer, MPTTModelAdmin)
