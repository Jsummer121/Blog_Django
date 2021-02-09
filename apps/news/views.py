from django.db.models import F
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from . import models
import logging
import json
from utils.res_code import to_json_data, error_map, Code

logger = logging.getLogger("django")


def my_login_required(func):
	def inner(request):
		if request.user.is_authenticated:
			return func(request)
		else:
			return redirect("/user/login")
	return inner


# @my_login_required
# @login_required(login_url='/user/login/')
def index(request):
	# only 把需要的字段添加进去
	tags = models.Tag.objects.only('id', 'name').filter(is_delete=False)
	hot_news = models.HotNews.objects.select_related('news').only('news__title', 'news__image_url', 'news_id').filter(is_delete=False).order_by('priority', '-news__clicks')[0:3]
	return render(request, "news/index.html", locals())



class NewsListView(View):
	def get(self, request):
		# 获取tag参数
		try:
			tag_id = int(request.GET.get("tag_id", 0))
		except Exception as e:
			logger.error("标签错误{}".format(e))
			tag_id = 0

		# 获取page参数
		try:
			page = int(request.GET.get("page", 1))
		except Exception as e:
			logger.error("页面错误{}".format(e))
			page = 1

		# 操作数据库
		# news_list = models.News.objects.select_related("tag", "author").only("id", "title", "image_url", "digest", "update_time", "tag__name", "author__username").filter(is_delete=False)  # select_related关联查询
		# ---------- 新方法 start-----------
		news_list = models.News.objects.values("id", "title", "image_url", "digest", "update_time").annotate(tag_name=F("tag__name"), author=F("author__username"))
		# ---------- 新方法 end-----------

		news = news_list.filter(is_delete=False, tag_id=tag_id) or news_list.filter(is_delete=False)

		# 分页  需要两个参数:一个待分页对象和一页的数量
		page_nt = Paginator(news, 4)

		# 返回当前页数据
		try:
			news_info = page_nt.page(page)
		except Exception as e:
			logger.error("给定的页码错误{}".format(e))
			news_info = page_nt.page(page_nt.num_pages)

		# 序列化输出
		# news_info_list = []
		# for n in news_info:
		# 	news_info_list.append({
		# 		"id": n.id,
		# 		"title": n.title,
		# 		"image_url": n.image_url,
		# 		"digest": n.digest,
		# 		"author": n.author.username,
		# 		"tag_name": n.tag.name,
		# 		"update_time": n.update_time
		# 	})
		data = {
			# "news": news_info_list,
			# ---------- 新方法 start-----------
			"news": list(news_info),
			# ---------- 新方法 end-----------
			"total_pages": page_nt.num_pages,
		}

		return to_json_data(data=data)


class NewsDetailView(View):
	def get(self, request, news_id):
		news = models.News.objects.select_related('tag', 'author').only('title', 'author__username', 'tag__name', 'content').filter(is_delete=False, id=news_id).first()
		comments = models.Comments.objects.select_related('author', 'parent').only('author__username', 'content', 'update_time', 'parent__update_time').filter(is_delete=False, news_id=news_id)
		comm_list = []
		for c in comments:
			comm_list.append(c.to_dict())
		if news:
			return render(request, 'news/news_detail.html', context={"news": news, "comm_list": comm_list})
		else:
			return HttpResponseNotFound("<h1>PAGE NOT FOUND</h1>")


class BannerView(View):
	def get(self, request):
		banners = models.Banner.objects.select_related('news').only('imgs_url', 'news__title', 'news_id').filter(is_delete=False)

		# 序列化输出
		banner_info = []
		for i in banners:
			banner_info.append({
				"news_title": i.news.title,
				"news_id": i.news.id,
				"imgs_url": i.imgs_url,
			})

		data = {
			"banners": banner_info
		}
		return to_json_data(data=data, )


class CommentsView(View):
	def post(self, request, news_id):
		"""
		3个参数
		news_id
		content
		parent_id

		1. 判断用户是否登录
		2. 获取参数
		3. 检验参数
		4. 保存到数据库
		:param request:
		:param news_id:
		:return:
		"""
		if not request.user.is_authenticated:
			return to_json_data(errno=Code.SESSIONERR, errmsg=error_map[Code.SESSIONERR])

		if not models.News.objects.only("id").filter(is_delete=False, id=news_id).exists():
			return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])

		# 获取参数
		json_data = request.body
		if not json_data:
			return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
		dict_data = json.loads(json_data)

		# 一级评论
		content = dict_data["content"]
		if not dict_data.get('content'):
			return to_json_data(errno=Code.PARAMERR, errmsg='评论内容不能为空')

		# 回复评论
		parent_id = dict_data.get('parent_id')
		try:
			if parent_id:
				if not models.Comments.objects.only('id').filter(is_delete=False, news_id=news_id, id=parent_id).exists():
					return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
		except Exception as e:
			logging.info('前台传的parent_id 异常：\n{}'.format(e))
			return to_json_data(errno=Code.PARAMERR, errmsg='未知异常')

		# 保存数据库
		news_content = models.Comments()
		news_content.content = content
		news_content.news_id = news_id
		news_content.author = request.user
		news_content.parent_id = parent_id if parent_id else None
		news_content.save()
		return to_json_data(data=news_content.to_dict())
