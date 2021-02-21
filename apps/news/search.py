# -*- coding: utf-8 -*-
# @Auther:Summer
"""
	该函数是用来实现索引的映射与创建
	详情：https://www.elastic.co/guide/en/elasticsearch/reference/7.10/indices-create-index.html
"""
from elasticsearch import Elasticsearch, helpers
import sys
import os
import django
# 添加当前路径到环境变量中
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd)  # 这里的路径要根据自己的目录结构来
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog_Django.settings')  # VueSt是自己的项目名称
django.setup()  # 更新配置
from models import News


class ES2:
	def __init__(self):
		self.es = Elasticsearch(["http://127.0.0.1:9200"])

	def create(self):
		"""
			创建映射
		:return:
		"""
		body = {
			"mappings":
				{"doc":
					{
						"properties": {
							"id": {"type": "long", "index": "false"},
							"title": {"type": "text", "analyzer": "ik_smart"},
							"digest": {"type": "text", "analyzer": "ik_smart"},
							"content": {"type": "text", "analyzer": "ik_smart"},
							"image_url": {"type": "keyword"}
						}
					}
				}, "settings": {
				"number_of_shards": 2,  # 分片数
		        "number_of_replicas": 0  # 副本数
		    },
		}
		# 创建索引
		self.es.indices.create(index="blog_django", body=body)
		print("索引创建成功")

	def bulk_write(self):
		"""
			批量写入
		:return:
		"""
		# 从模型中获取全部数据
		query_obj = News.objects.all()

		# 将数据进行格式化
		action = [
			{
				"_index": "blog_django",
				"_source": {
					"id": i.id,
					"title": i.title,
					"digest": i.digest,
					"content": i.content,
					"image_url": i.image_url
				}
			}
			for i in query_obj]

		# 批量写入数据
		helpers.bulk(self.es, action, request_timeout=1000)
		print("数据输入成功")


if __name__ == '__main__':
	es = ES2()
	es.create()
	es.bulk_write()
