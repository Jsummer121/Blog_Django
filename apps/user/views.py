from django.shortcuts import render
from django.views import View
from django.contrib.auth import login

import json
from .forms import RegisterForm
from utils.res_code import to_json_data, Code, error_map
from .models import Users


class LoginView(View):
	def get(self, request):
		return render(request, "users/login.html")


class RegistarView(View):
	"""
	username
	password
	password_repeat
	mobile
	sms_code
	"""
	def get(self, request):
		return render(request, "users/register.html")

	def post(self, request):
		json_data = request.body()
		if not json_data:
			return to_json_data(errno=Code.PARAMERR, errmsg=[error_map[Code.PARAMERR]])
		data_dict = json.loads(json_data.decode('utf8'))
		# 表单校验
		form = RegisterForm(data=data_dict)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			mobile = form.cleaned_data.get("mobile")
			user = Users.objects.create_user(username=username, password=password, mobile=mobile)
			login(request, user)
			return to_json_data(errmsg="恭喜你，注册成功")
		else:
			error_map_list = []
			for item in form.errors.values():
				error_map_list.append(item[0])
			err_str = "/".join(error_map_list)
			return to_json_data(errno=Code.PARAMERR, errmsg=err_str)
