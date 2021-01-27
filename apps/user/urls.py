# -*- coding: utf-8 -*-
# @Author  : summer
from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
	path("login/", views.LoginView.as_view(), name="login"),
	path("register/", views.RegistarView.as_view(), name="register"),
	path("findpwd/", views.FindPswView.as_view(), name="findpwd"),
	path("logout/", views.LogoutView.as_view(), name="logout"),
]
