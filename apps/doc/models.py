from django.db import models
from utils.BaseModel import ModelBase


class Docs(ModelBase):
	"""
	文件地址
	书籍的标题
	书籍的描述信息
	书籍的封面图
	作者
	"""
	file_url = models.URLField("文件地址", help_text="书籍地址")
	title = models.CharField("书籍标题", max_length=150)
	desc = models.TextField("书籍描述")
	image_url = models.URLField("书籍封面", default="")
	auther = models.ForeignKey("user.Users", on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = "tb_docs"
		verbose_name = "书籍"

	def __str__(self):
		return self.title
