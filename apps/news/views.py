from django.db.models import F
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from . import models
import logging
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
		if news:
			return render(request, 'news/news_detail.html', context={"news": news})
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

