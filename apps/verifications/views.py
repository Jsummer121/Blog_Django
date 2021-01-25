from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from user.models import Users

from utils.captcha.captcha import captcha
from utils.res_code import to_json_data
from django_redis import get_redis_connection
import logging

logger = logging.getLogger("django")


# 图形验证
class ImageCode(View):
	def get(self, request, image_code):
		text, image = captcha.generate_captcha()

		# 将产生的uuid放入redis
		## 1.连接数据库
		con_redis = get_redis_connection("verify_codes")
		## 2.配置key
		redis_key = "img_{}".format(image_code)
		## 3.设置过期时间
		con_redis.setex(redis_key, 300, text)

		logger.info("IMAGE_CODE {}".format(text))
		return HttpResponse(content=image, content_type="image/jpg")


# 用户名校验
class UsernameView(View):
	def get(self, request, username):
		data = {
			"username": username,
			"count": Users.objects.filter(username=username).count(),
		}
		# return JsonResponse({"data": data})
		return to_json_data(data=data)
