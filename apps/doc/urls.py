# -*- coding: utf-8 -*-
# @Auther:Summer
from django.urls import path
from . import views

app_name = "doc"

urlpatterns = [
	path("", views.doc),
	path("download/<int:doc_id>", views.DocDownload.as_view(), name="download"),
]
