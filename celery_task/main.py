# -*- coding: utf-8 -*-
# @Auther:Summer
from celery import Celery

# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'Blog_Django.settings'

# 创建celery应用/实例
app = Celery('send_sms')

# 导入celery配置
app.config_from_object('celery_task.config')

# 自动注册celery任务
app.autodiscover_tasks(['celery_task.sms'])
