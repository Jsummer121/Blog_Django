# -*- coding: utf-8 -*-
# @Auther:Summer
# 图片验证码redis有效期，单位秒
IMAGE_CODE_REDIS_EXPIRES = 5 * 60

# 短信验证码有效期，单位分钟
SMS_CODE_REDIS_EXPIRES = 5 * 60

# 发送间隔
SEND_SMS_CODE_INTERVAL = 60

# 存储过期时间的值（随机）
EXPIRE_VALUE = 1

# 短信发送模板
SMS_CODE_TEMP_ID = 1

# 短信发送时间
SMS_CODE_TEMP = 5

# 随机的短信验证码
SMS_CODE_LIT = 0
SMS_CODE_BIG = 999999
