# -*- coding: utf-8 -*-
# @Auther:Summer
from django.db import models


class ModelBase(models.Model):
	# 数据创建时间
	create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
	# 更新时间
	update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
	# 逻辑删除字段
	is_delete = models.BooleanField(default=False, verbose_name="逻辑删除")

	class Meta:
		abstract = True  # 指明该类为抽象类，当进行数据迁移时，这个表不会被创建
