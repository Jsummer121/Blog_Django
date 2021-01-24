# -*- coding: utf-8 -*-
# @Author  : summer
from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
	path("", views.demo, name="demo"),
]
