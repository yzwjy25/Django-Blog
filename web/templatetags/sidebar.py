from django_redis import get_redis_connection
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
from django.template import Library
from django.utils.safestring import mark_safe
from django.urls import reverse
from web.models import Category, Blog
from web.service.myurl import withparam_url

register = Library()



@register.simple_tag(name='categories')
def categories(request):
    # 分组查询
    # cates = Category.objects.annotate(num=Count('blog')).values('id', 'title', 'num')
    cates = Category.objects.all().values('id', 'title')
    url = reverse("article")
    html = f'<li data-index="1"><a href="{url}">全部文章</a></li>'
    for index, item in enumerate(cates, 2):
        # url = reverse("article")
        url = withparam_url(request, "article", "category", item['id'])
        html += f'<li data-index="{index}"><a href="{url}">{item["title"]}</a></li>'
    # print(html)
    return mark_safe(html)

@register.simple_tag(name='categories_moblie')
def categories_moblie(request):
    # 分组查询
    cates = Category.objects.annotate(num=Count('blog')).values('id', 'title', 'num')
    url = reverse("article")
    html = f'<a href="{url}">全部文章</a>'
    for index, item in enumerate(cates, 2):
        # url = reverse("article")
        url = withparam_url(request, "article", "category", item['id'])
        html += f'<a href="{url}">{item["title"]}</a>'
    # print(html)
    return mark_safe(html)

# @register.simple_tag(name='yearmonth')
# def yearmonth():
#     # 分组查询
#     # blogs = Blog.objects.filter().values('id', 'title')
#     blogs = Blog.objects.annotate(year=TruncYear('publish_time')).values('year').annotate(
#         month=TruncMonth('publish_time')).values('month').annotate(num=Count('id')).order_by('-month').values('month', 'num')
#     # print(blogs)
#     html = ""
#
#     for item in blogs:
#         html += "<li><a href=\"\\?year={}&month={}\">{}({})</a></li>".format(item['month'].year, item['month'].month,item['month'].strftime('%Y-%m'), item['num'])
#     # print(html)
#     return mark_safe(html)

@register.simple_tag(name='read_rank')
def read_rank():
    # 分组查询
    # blogs = Blog.objects.filter().values('id', 'title')
    blogs = Blog.objects.filter().order_by('-read_count')[:6].values('id', 'title', 'read_count')
    # print(blogs)
    '<li> <a href="/Blog/Read/9">SpringBoot 入门爬虫项目实战</a></li>'
    html = ""
    # conn = get_redis_connection("default")
    # blogs = []
    # for item in conn.zrange('read_count', 0, 10, desc=True):
    #     item = item.decode()
    #     blog_id, blog_title = item.split(":")
    #     read_count = int(conn.zscore('read_count', item))
    #     blogs.append(
    #         {
    #             "id":blog_id,
    #             "title":blog_title,
    #             "read_count":read_count
    #         }
    #     )
    for item in blogs:
        # print(item)
        # url = reverse("detial", int(item['id']))
        html += f'<li> <a href="{item["id"]}">{item["title"]}({item["read_count"]})</a></li>'
        # html += "<li><a href=\"\\article\\{}\">{}({})</a></li>".format(item['id'], item['title'][:10] + "..." if len(item['title']) > 10 else item['title'], item['read_count'])
    # print(html)
    return mark_safe(html)

