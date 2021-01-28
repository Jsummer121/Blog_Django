from django.http import HttpResponse
from django.shortcuts import render
from .models import Tag

# Create your views here.


def index(request):
	# only 把需要的字段添加进去
	tags = Tag.objects.only('id','name').filter(is_delete=False)
	return render(request, "news/index.html", locals())
