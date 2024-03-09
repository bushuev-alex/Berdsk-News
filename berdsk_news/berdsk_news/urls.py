"""
URL configuration for berdsk_news project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import RedirectView
from django.views.static import serve
from berdsk_news import settings
from django.views.generic.base import TemplateView
from django.contrib.sitemaps.views import sitemap
from news.sitemap import StaticViewSitemap, DynamicViewNews

sitemaps = {
   'static': StaticViewSitemap,
   'news': DynamicViewNews,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path("", include('news.urls')),
    path("", RedirectView.as_view(url="news/"), name="news"),

    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),

    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

]
