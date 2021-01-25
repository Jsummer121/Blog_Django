from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from utils.captcha.captcha import captcha
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
