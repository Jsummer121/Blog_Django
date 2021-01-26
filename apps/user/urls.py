# -*- coding: utf-8 -*-
# @Author  : summer
from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
	path("login/", views.login, name="login"),
	path("register/", views.RegistarView.as_view(), name="register"),
]
