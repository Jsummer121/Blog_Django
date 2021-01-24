from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as _UserManager


class UserManager(_UserManager):
	def create_superuser(self, username, password, email=None, **extra_fields):
		super().create_superuser(username=username, email=email, password=password, **extra_fields)


# Create your models here.
class Users(AbstractUser):
	objects = UserManager()

	mobile = models.CharField(verbose_name="手机号", max_length=20, unique=True, error_messages={'unique': "手机号已注册"})
	email_ac = models.BooleanField(default=False, verbose_name="邮箱状态")
	REQUIRED_FIELDS = ['mobile']

	class Meta:
		db_table = "tb_users"  # 设置数据库名，默认是类名
		verbose_name = "用户"

	def __str__(self):
		return self.username
