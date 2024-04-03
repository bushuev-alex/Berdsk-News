# import time

from django.views.generic import ListView, TemplateView  # , DetailView, CreateView, UpdateView, DeleteView,
from django.contrib import messages
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse  # Http404

# from django.shortcuts import render
# from django.template.loader import render_to_string
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.utils.translation import gettext
# from django.utils import timezone
# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
# from django.urls import reverse, reverse_lazy
# from django.views import View

# from django.conf import settings
# from pprint import pprint
# import pytz

from datetime import datetime, timedelta, timezone
from .models import News, Category, Origin, Tag, Advertisement  # , Comment
from news.forms import AdForm


class MainPage(TemplateView):
    template_name = 'flatpages/index/index.html'
    week_ago = datetime.now() - timedelta(days=7)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.order_by("-rating")
        context["tags"] = Tag.objects.order_by("-rating")
        context["origins"] = Origin.objects.all()
        context["advertisements"] = Advertisement.objects.all()

        news_week_ago = News.objects.filter(published_at__gte=self.week_ago)
        context["latest_news"] = news_week_ago.order_by("-id")[:7]
        trending_news = news_week_ago.order_by('-rating')[:6]
        context["enum_trending_news"] = enumerate(trending_news)
        return context


class DetailPage(TemplateView):
    template_name = 'flatpages/single_post/single-post.html'
    week_ago = datetime.now() - timedelta(days=7)

    # def get(self):
    #     pass

    def get_context_data(self, **kwargs):
        try:
            pk = kwargs['pk']
            News.objects.get(id=pk)
        except News.DoesNotExist:
            pk = News.objects.latest("pk").id
        context = super().get_context_data(**kwargs)
        context["single_news"] = News.objects.get(id=pk)
        # context["comments"] = Comment.objects.filter(news_id=pk)  # .order_by("id")
        context["categories"] = Category.objects.order_by("-rating")[:15]
        context["tags"] = Tag.objects.order_by("name", "-rating")[:15]
        context["origins"] = Origin.objects.order_by("id", "-rating")

        latest_news = News.objects.order_by("-published_at")[:6]
        context["latest_news"] = latest_news
        context["enum_latest_news"] = enumerate(latest_news)

        trending_news = News.objects.filter(published_at__gte=self.week_ago).order_by('-rating')[:6]
        context["enum_trending_news"] = enumerate(trending_news)

        interesting_news = News.objects.order_by('-rating')[:6]
        context["enum_interesting_news"] = enumerate(interesting_news)

        return context


class BaseListPage(ListView):
    context_object_name = "news_list"
    paginate_by = 10
    week_ago = datetime.now() - timedelta(days=7)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.order_by("-rating")
        context["tags"] = Tag.objects.order_by("-rating")[:15]
        context["origins"] = Origin.objects.order_by("id")

        context["latest_news"] = News.objects.order_by("-published_at")[:6]
        context["trending_news"] = News.objects.filter(published_at__gte=self.week_ago).order_by('-rating')[:6]
        context["interesting_news"] = News.objects.order_by('-rating')[:6]

        return context


class CategoryListPage(BaseListPage):
    template_name = 'flatpages/category/category.html'

    def get_queryset(self):
        return News.objects.filter(category=self.kwargs['pk']).order_by("-published_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(id=self.kwargs['pk'])
        return context


class AllCategoriesListPage(TemplateView):
    template_name = 'flatpages/category/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["categories"] = Category.objects.all()
        context["origins"] = Origin.objects.all()
        context["latest_news"] = News.objects.order_by("-id")[:7]
        return context


class TagListPage(BaseListPage):
    template_name = 'flatpages/tag/tag.html'

    def get_queryset(self):
        return News.objects.filter(tag=self.kwargs['pk']).order_by("-published_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = Tag.objects.get(id=self.kwargs['pk'])
        return context


class AllTagsListPage(TemplateView):
    template_name = 'flatpages/tag/tags.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["categories"] = Category.objects.all()
        context["origins"] = Origin.objects.all()
        context["latest_news"] = News.objects.order_by("-id")[:7]
        return context


class OriginListPage(BaseListPage):
    template_name = 'flatpages/origin/origin.html'

    def get_queryset(self):
        return News.objects.filter(parsed_from=self.kwargs['pk']).order_by("-published_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["origin"] = Origin.objects.get(id=self.kwargs['pk'])
        return context


class AllOriginsListPage(TemplateView):
    template_name = 'flatpages/origin/origins.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["categories"] = Category.objects.all()
        context["origins"] = Origin.objects.all()
        context["latest_news"] = News.objects.order_by("-id")[:7]
        return context


class ContactPage(TemplateView):
    template_name = 'flatpages/contacts/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.order_by("-rating")
        context["origins"] = Origin.objects.all()
        context["tags"] = Tag.objects.all()
        context["latest_news"] = News.objects.order_by("-id")[:7]
        return context

    def post(self, request, *args, **kwargs):
        form = AdForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(self.request, message="Ваше сообщение отправлено. Спасибо!")
            return HttpResponseRedirect("/contacts")
        else:
            print(form.cleaned_data)
            print(form.errors.values())
            for error in list(form.errors.values()):
                messages.error(self.request, message=error)  # HttpResponse("Неверные данные")
            return HttpResponseRedirect("/contacts")


class About(TemplateView):
    template_name = 'flatpages/about/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().order_by("-rating")
        context["origins"] = Origin.objects.all()
        context["latest_news"] = News.objects.order_by("-id")[:7]
        return context


class SearchListPage(BaseListPage):

    template_name = 'flatpages/search/search.html'

    def get_queryset(self):
        search_word = self.kwargs["search_word"]
        print(self.kwargs)
        print(search_word)
        return News.objects.filter(full_text__icontains=search_word).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_word"] = self.kwargs["search_word"]
        # context["search_result"] = Category.objects.get(id=self.kwargs['pk'])
        return context


def redirect_to_search_result(request, **kwargs):
    search_word: str = request.GET["search_word"]
    return redirect(to=f"/news/search/{search_word}/")
