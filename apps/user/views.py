from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import login, logout

import json
from .forms import RegisterForm, ChangePswForm, LoginForm
from utils.res_code import to_json_data, Code, error_map
from .models import Users


class LoginView(View):
	def get(self, request):
		return render(request, 'users/login.html')

	def post(self, request):
		"""
	    用户名或者手机号
	    密码
	    是否记住我
	    :param request:
	    :return: to_json_data
	    """
		json_data = request.body  # 获取数据
		if not json_data:  # 判断诗句是否为空
			return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
		dict_data = json.loads(json_data.decode("utf8"))  # 转化成字典格式
		form = LoginForm(data=dict_data, request=request)
		if form.is_valid():
			return to_json_data(errmsg="恭喜你，登陆成功")
		else:
			error_map_list = []
			for item in form.errors.values():
				error_map_list.append(item[0])
			err_str = "/".join(error_map_list)
			return to_json_data(errno=Code.PARAMERR, errmsg=err_str)


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
		json_data = request.body
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


class FindPswView(View):
	def get(self, request):
		return render(request, 'users/findpsw.html')

	def post(self, request):
		json_data = request.body
		if not json_data:
			return to_json_data(errno=Code.PARAMERR, errmsg=[error_map[Code.PARAMERR]])
		data_dict = json.loads(json_data.decode("utf8"))
		form = ChangePswForm(data=data_dict)
		if form.is_valid():
			mobile = form.cleaned_data.get("mobile")
			password = form.cleaned_data.get("password")
			user = Users.objects.get(mobile=mobile)
			user.set_password(password)
			user.save()
			return to_json_data(errmsg="密码修改成功")

		else:
			error_map_list = []
			for item in form.errors.values():
				error_map_list.append(item)
			err_str = "/".join(error_map_list)
			return to_json_data(errno=Code.PARAMERR, errmsg=err_str)


class LogoutView(View):
	def get(self, request):
		logout(request)
		return redirect(reverse("user:login"))
