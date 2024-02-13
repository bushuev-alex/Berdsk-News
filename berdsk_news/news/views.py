# from django.shortcuts import render
# from django.template.loader import render_to_string
from django.views.generic import ListView, TemplateView  # , DetailView, CreateView, UpdateView, DeleteView,
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.utils.translation import gettext
# from django.utils import timezone
# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
# from django.urls import reverse, reverse_lazy
# from django.http import Http404, HttpResponse
# from django.views import View
# from django.shortcuts import render, reverse, redirect, get_object_or_404
# from django.conf import settings

from datetime import datetime, timedelta, timezone
# from pprint import pprint
# import pytz

from .models import News, Category, Origin, Tag  # , Comment


class MainPage(TemplateView):
    template_name = 'flatpages/index/index.html'
    week_ago = datetime.now() - timedelta(days=7)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().order_by("-rating")
        context["origins"] = Origin.objects.all()
        context["latest_news"] = News.objects.all().order_by("-id")[:7]
        trending_news = News.objects.all().filter(published_at__gte=self.week_ago).order_by('-rating')[:5]
        context["enum_trending_news"] = enumerate(trending_news)
        return context


class DetailPage(TemplateView):
    template_name = 'flatpages/single_post/single-post.html'
    week_ago = datetime.now() - timedelta(days=7)

    def get_context_data(self, **kwargs):
        pk = kwargs['pk']
        context = super().get_context_data(**kwargs)
        context["single_news"] = News.objects.get(id=pk)
        # context["comments"] = Comment.objects.filter(news_id=pk)  # .order_by("id")
        context["categories"] = Category.objects.all().order_by("-rating")[:15]
        context["tags"] = Tag.objects.all().order_by("name", "-rating")[:15]
        context["origins"] = Origin.objects.all().order_by("id", "-rating")

        latest_news = News.objects.all().order_by("-published_at")[:6]
        context["latest_news"] = latest_news
        context["enum_latest_news"] = enumerate(latest_news)

        trending_news = News.objects.all().filter(published_at__gte=self.week_ago).order_by('-rating')[:6]
        context["enum_trending_news"] = enumerate(trending_news)

        interesting_news = News.objects.all().order_by('-rating')[:6]
        context["enum_interesting_news"] = enumerate(interesting_news)

        return context


class BaseListPage(ListView):
    context_object_name = "news_list"
    paginate_by = 10
    week_ago = datetime.now() - timedelta(days=7)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all().order_by("-rating")
        context["tags"] = Tag.objects.all().order_by("-rating")[:15]
        context["origins"] = Origin.objects.all().order_by("id")

        context["latest_news"] = News.objects.all().order_by("-published_at")[:6]
        context["trending_news"] = News.objects.all().filter(published_at__gte=self.week_ago).order_by('-rating')[:6]
        context["interesting_news"] = News.objects.all().order_by('-rating')[:6]

        return context


class CategoryListPage(BaseListPage):
    template_name = 'flatpages/category/category.html'

    def get_queryset(self):
        return News.objects.filter(category=self.kwargs['pk']).order_by("-published_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(id=self.kwargs['pk'])
        return context


class OriginListPage(BaseListPage):
    template_name = 'flatpages/origin/origin.html'

    def get_queryset(self):
        return News.objects.filter(parsed_from=self.kwargs['pk']).order_by("-published_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["origin"] = Origin.objects.get(id=self.kwargs['pk'])
        return context


class ContactPage(TemplateView):
    template_name = 'flatpages/contacts/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().order_by("-rating")
        context["origins"] = Origin.objects.all()
        context["latest_news"] = News.objects.all().order_by("-id")[:7]
        return context


class About(TemplateView):
    template_name = 'flatpages/about/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().order_by("-rating")
        context["origins"] = Origin.objects.all()
        context["latest_news"] = News.objects.all().order_by("-id")[:7]
        return context
