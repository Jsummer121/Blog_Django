# -*- coding: utf-8 -*-
# @Author  : summer
from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
	path("", views.index, name="index"),
	path("news/", views.NewsListView.as_view(), name="news_list"),
	path("news/<int:news_id>/", views.NewsDetailView.as_view(), name="news_detail"),
	path("news/banners/", views.BannerView.as_view(), name="news_banners"),
	path("news/<int:news_id>/comments/", views.CommentsView.as_view(), name="comments"),
	# path("indeses", views.es2, name="indeses"),
	path("search/", views.SearchView.as_view(), name="search")
]
