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
from django.urls import path, include
from django.shortcuts import redirect

from news.views import (MainPage,
                        DetailPage,
                        CategoryListPage,
                        OriginListPage,
                        ContactPage,
                        About,
                        AllCategoriesListPage,
                        AllOriginsListPage,
                        SearchListPage,
                        redirect_to_search_result)

urlpatterns = [
    path("news/", MainPage.as_view(), name='news'),
    path("news/search/", redirect_to_search_result, name='to_search_result'),
    path("news/search//", lambda request: redirect("/contacts/")),
    path("news/search/<str:search_word>/", SearchListPage.as_view(), name='search_result'),
    path("news/<int:pk>/", DetailPage.as_view(), name='news_by_id'),
    path("news/categories/", AllCategoriesListPage.as_view(), name='categories'),
    path("news/category/<int:pk>/", CategoryListPage.as_view(), name='category'),
    path("news/origins/", AllOriginsListPage.as_view(), name='origins'),
    path("news/origin/<int:pk>/", OriginListPage.as_view(), name='origin'),
    path("contacts/", ContactPage.as_view(), name='contacts'),
    path("about/", About.as_view(), name='about')
]
