# -*- coding: utf-8 -*-
# @Auther:Summer
from django.middleware.csrf import get_token
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

from user.models import Users


class Middleware(MiddlewareMixin):
	def process_request(self, request):
		get_token(request)


def middleware(get_response):
	# 这个地方编写的代码会在第一次执行，也就是初始化的时候
	print("__init__")

	def middleware(request):
		# 这个地方会在试图处理之前执行
		print("视图请求之前")
		response = get_response(request)
		# 这个地方会在视图处理执行执行，也就是响应得到的时候
		print("视图处理之前")
		return response
	return middleware


# 针对于没有登录访问页面
class LoginMiddleware(MiddlewareMixin):
	def process_request(self, request):
		if request.path in ['/']:
			userid = request.user.id
			user = Users.objects.filter(id=userid).first()
			if user:
				request.user = user
			else:
				return redirect("/user/login/")
