# -*- coding: utf-8 -*-
# @Auther:Summer
from django.urls import path,re_path
from . import views

app_name = "verifications"

urlpatterns = [
	path("image_code/<uuid:image_code>/", views.ImageCode.as_view(), name="image_code"),
	re_path(r"username/(?P<username>\w{5,20})/", views.UsernameView.as_view(), name="username")
]
