# -*- coding: utf-8 -*-
# @Auther:Summer
from celery_task.main import app
from utils.yuntongxun.sms import CCP

import logging

logger = logging.getLogger("django")


@app.task(name='send_sms_code')
def send_sms_code(mobile, sms_num, expires, temp_id):
    """
    发送短信验证码
    :param mobile: 手机号
    :param sms_num: 验证码
    :param expires: 有效期
    :return: None
    """
    try:
        result = CCP().send_template_sms(mobile, [sms_num, expires], temp_id)

    except Exception as e:
        logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))

    else:
        if result == 0:
            logger.info("发送验证码短信[正常][ mobile: %s sms_code: %s]" % (mobile, sms_num))
        else:
            logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)