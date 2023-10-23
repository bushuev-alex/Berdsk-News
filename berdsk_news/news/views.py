from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponse
from django.views import View
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.conf import settings

from datetime import datetime
from pprint import pprint

from .models import News, Category, Comment, CmntToCmnt


class MainPage(TemplateView):
    template_name = 'flatpages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sliced_news"] = News.objects.all().order_by("-id")[:4]
        context["categories"] = Category.objects.all().order_by("name")
        context["latest_news"] = News.objects.all().order_by("-id")[:5]
        return context


class DetailPage(TemplateView):
    template_name = 'flatpages/single-post.html'

    def get_context_data(self, **kwargs):
        pk = kwargs['pk']
        context = super().get_context_data(**kwargs)
        context[f"single_news"] = News.objects.get(id=pk)
        context[f"comments"] = Comment.objects.filter(news_id=pk)
        context["categories"] = Category.objects.all().order_by("name")
        context["latest_news"] = News.objects.all().order_by("-id")[:5]
        return context
