from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from news.models import News


class StaticViewSitemap(Sitemap):
    changefreq = "hourly"
    protocol = "http"

    def items(self):
        return ['news']

    def location(self, item):
        return reverse(item)


class DynamicViewNews(Sitemap):
    changefreq = "daily"
    protocol = "http"
    pagination = 100

    def items(self):
        return News.objects.all().order_by("-id")
