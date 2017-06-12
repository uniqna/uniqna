from django.contrib.sitemaps import Sitemap
from ask.models import Question


class ThreadsSitemap(Sitemap):
    changefreq = "always"
    priority = 1.0

    def items(self):
        return Question.objects.all()
