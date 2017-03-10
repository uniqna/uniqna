from django.contrib.sitemaps import Sitemap
from ask.models import question


class ThreadsSitemap(Sitemap):
    changefreq = "always"
    priority = 1.0

    def items(self):
        return question.objects.all()
