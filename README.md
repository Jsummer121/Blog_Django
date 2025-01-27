# Blog_Django
## 1、网站类型
本项目主要完成一个个人新闻博客类网站，用于知识分享，交友互动等

## 2、主页模块

- 轮播图
- 热门文章推荐
- 文章标签、文章列表（可加载更多）
- 左侧广告展示
- 个人联系方式

## 3、用户模块

- 注册
    - 短信验证码（云通信平台）
    - 图片验证码
- 登录
    - 用户名和手机号登录
- 个人中心页

## 4、在线视频模块

实现在线播放视频功能，用于福利课视频展示等。

## 5、文件下载模块

实现相关资源共享，如课件笔记等。

## 6、搜索模块
使用流行的elasticsearch收缩引擎框架，实现网站资源快速搜索定位功能。

## 7、后台管理模块

- 文章标签管理
- 文章发布
- 文章管理
- 热门文章管理
- 主页轮播图管理
- 课程发布
- 文档上传
- 账号管理

# 项目架构

## 1、网站开发模式

**前后端部分分离的开发模式**



## 2、前端技术

html + css + js + jquery(ajax)



## 3、后端技术

Django2.1 + Django restframework + mysql + redis + celery(可能会拓展) + elaticsearch + nginx + uwsgi


| 技术点       | 说明                                |
| ------------ | ----------------------------------- |
| Mysql        | 双机热备、读写分离                  |
| redis        | session缓存、图片验证码、短信验证码 |
| elaticsearch | 站内搜索                            |
| celery       | 异步发送短信                        |


