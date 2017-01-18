from django.db import models


class question(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    answers = models.IntegerField(default=0)
    author = models.CharField(max_length=100, default="anonymous")
    created_time = models.DateTimeField(auto_now_add=True);

    def __str__(self):
        return (self.title);

    def get_time(self):
        t = self.created_time;
        return "{}-{}-{} {}:{}".format(t.day, t.month, t.year, t.hour, t.minute);
