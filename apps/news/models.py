from django.db import models
from utils.BaseModel import ModelBase


# 文章分类
class Tag(ModelBase):
    name = models.CharField(max_length=64, verbose_name="文章分类名")  # 一个中文就有三个字节

    class Meta:
        ordering = ['-update_time', '-id']  # 设置排序
        db_table = "tb_tag"  # 设置表名
        verbose_name = "新闻分类标签"  # 设置别名

    def __str__(self):
        return self.name


class News(ModelBase):
    title = models.CharField(max_length=150, verbose_name="标题", help_text="标题")
    digest = models.CharField(max_length=200, verbose_name="摘要", help_text="摘要")
    content = models.TextField(verbose_name="内容", help_text="内容")
    clicks = models.IntegerField(default=0, verbose_name="点击量", help_text="点击量")
    image_url = models.URLField(default="", verbose_name="图片url", help_text="图片url")
    tag = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('user.Users', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = "tb_news"  # 指明数据库表名
        verbose_name = "新闻"  # 在admin站点中显示的名称

    def __str__(self):
        return self.title


class Comments(ModelBase):
    content = models.TextField(verbose_name="内容", help_text="内容")

    author = models.ForeignKey('user.Users', on_delete=models.SET_NULL, null=True)
    news = models.ForeignKey('News', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = "tb_comments"  # 指明数据库表名
        verbose_name = "评论"  # 在admin站点中显示的名称

    def __str__(self):
        return '<评论{}>'.format(self.id)


class HotNews(ModelBase):
    PRI_CHORIES = [
        (1, "第一级"),
        (2, "第二级"),
        (3, "第三级")
    ]
    priority = models.IntegerField(choices=PRI_CHORIES, verbose_name="优先级", help_text="优先级")
    news = models.OneToOneField('News', on_delete=models.CASCADE)


    class Meta:
        ordering = ['-update_time', '-id']
        db_table = "tb_hot"  # 指明数据库表名
        verbose_name = "热门新闻"  # 在admin站点中显示的名称

    def __str__(self):
        return '<热门新闻{}>'.format(self.id)


# 轮播图
class Banner(ModelBase):
    PRI_CHOICE = [  # 设置优先级列表
        (1, "第一级"),
        (2, "第二级"),
        (3, "第三级"),
        (4, "第四级"),
        (5, "第五级"),
        (6, "第六级"),
    ]

    imgs_url = models.URLField(verbose_name="轮播图的url")  # 设置图片的url
    priority = models.IntegerField(choices=PRI_CHOICE, default=6, verbose_name="轮播图的优先级")  # 设置轮播图优先级
    news = models.OneToOneField('News', on_delete=models.CASCADE)  # 主表删除，从表也自动删除

    class Meta:
        db_table = "tb_banner"
        verbose_name = "轮播图"
        ordering = ["-update_time", "-id"]

    def __str__(self):
        return "<轮播图{}>".format(self.id)
