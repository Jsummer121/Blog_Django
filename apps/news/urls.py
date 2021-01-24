# -*- coding: utf-8 -*-
# @Author  : summer
from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
	path("", views.index, name="index"),
	path("<int:a_id>", views.res, name="res"),
]
