# -*- coding: utf-8 -*-
# @Auther:Summer
from django.urls import path
from . import views

app_name = "verifications"

urlpatterns = [
	path("image_code/<uuid:image_code>/", views.ImageCode.as_view(), name="image_code"),
]

