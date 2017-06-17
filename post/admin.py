from django.contrib import admin

from post.models import Channel, Question


class question_admin(admin.ModelAdmin):
    list_display = ('id', 'title', 'answers',
                    'author', 'created_time', 'solved')
    filter_horizontal = ('ups', 'downs')


admin.site.register(Question, question_admin)
admin.site.register(Channel)
