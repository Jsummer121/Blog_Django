from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, FileResponse, Http404
from django.utils.encoding import escape_uri_path

from .models import Docs
from Blog_Django.settings import DOC_FILE_URL
import requests


def doc(request):
	docs = Docs.objects.only("image_url", "title", "desc").filter(is_delete=False)
	return render(request, "doc/docDownload.html", context={"docs":docs})


class DocDownload(View):
	def get(self, request, doc_id):
		doc_file = Docs.objects.only("file_url").filter(is_delete=False,id=doc_id).first()
		if doc_file:
			doc_url = doc_file.file_url
			doc_url = DOC_FILE_URL + doc_url

			# res = HttpResponse(requests.get(doc_url))  # 如果使用这个，可能会产生文件过大而导致系统堵塞
			res = FileResponse(requests.get(doc_url))  # 分批写入用户的内存，一个批次4096

			# 获取尾坠，查看格式
			ex_name = doc_url.split(".")[-1]

			if not ex_name:
				raise Http404("文件名异常")
			else:
				ex_name = ex_name.lower()

			if ex_name == 'pdf':
				res['Content-type'] = 'application/pdf'

			elif ex_name == 'doc':
				res['Content-type'] = 'application/msowrd'

			elif ex_name == 'ppt':
				res['Content-type'] = 'application/powerpoint'

			else:
				raise Http404('文件格式不正确')

			doc_filename = escape_uri_path(doc_url.split("/")[-1])

			# attachment  保存  inline 显示
			res["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(doc_filename)
			return res

		else:
			raise Http404('文档不存在')
