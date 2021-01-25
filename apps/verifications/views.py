import json
import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from user.models import Users

from utils.captcha.captcha import captcha
from utils.res_code import to_json_data, Code, error_map
from django_redis import get_redis_connection
from .forms import FromRegister
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


# 手机号校验
class MobileView(View):
	def get(self, request, mobile):
		data = {
			"mobile": mobile,
			"count": Users.objects.filter(mobile=mobile).count()
		}
		return to_json_data(data=data)


# 发送短信验证码
class SmsCode(View):
	def post(self, request):
		" mobile  text  iamge_code_id"
		json_str = request.body
		if not json_str:
			return to_json_data(errno=Code.PARAMERR, errmsg='参数为空')
		dict_data = json.loads(json_str)
		form = FromRegister(data=dict_data)

		# 进行数据校验
		if form.is_valid():
			mobile = form.cleaned_data.get('mobile')
			# 生成6位短信验证码
			sms_num = '%06d' % random.randint(0, 999999)

			# 构建外键
			con_redis = get_redis_connection('verify_codes')
			# 短信建  5分钟  sms_num
			sms_text_flag = "sms_{}".format(mobile).encode('utf8')
			# 过期时间
			sms_flag_fmt = 'sms_flag_{}'.format(mobile).encode('utf8')
			# 存
			con_redis.setex(sms_text_flag, 300, sms_num)
			con_redis.setex(sms_flag_fmt, 60, 1)  # 过期时间  1

			# 发送短信
			logger.info('短信验证码：{}'.format(sms_num))

			# 调用接口发送短信
			try:
				result = 0
			except Exception as e:
				logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
				return to_json_data(errno=Code.SMSERROR, errmsg=error_map[Code.SMSERROR])
			else:
				if result == 0:
					logger.info("发送验证码短信[正常][ mobile: %s sms_code: %s]" % (mobile, sms_num))
					return to_json_data(errmsg='短信发送正常')
				else:
					logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)
					return to_json_data(errno=Code.SMSFAIL, errmsg=error_map[Code.SMSFAIL])

		else:
			err_msg_list = []
			for item in form.errors.get_json_data().values():
				err_msg_list.append(item[0].get('message'))
			err_msg_str = '/'.join(err_msg_list)
			return to_json_data(errno=Code.PARAMERR, errmsg=err_msg_str)
