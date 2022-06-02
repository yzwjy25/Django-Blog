from django_redis import get_redis_connection
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
from django.template import Library
from django.utils.safestring import mark_safe

from web.models import Category, Blog

register = Library()


@register.simple_tag(name='categories')
def categories():
    # 分组查询
    cates = Category.objects.annotate(num=Count('blog')).values('id', 'title', 'num')

    html = "<li><a href=\"\\\">全部</a></li>"
    for item in cates:
        html += "<li><a href=\"\\?category={}\">{}({})</a></li>".format(item['id'], item['title'], item['num'])
    # print(html)
    return mark_safe(html)


@register.simple_tag(name='yearmonth')
def yearmonth():
    # 分组查询
    # blogs = Blog.objects.filter().values('id', 'title')
    blogs = Blog.objects.annotate(year=TruncYear('publish_time')).values('year').annotate(
        month=TruncMonth('publish_time')).values('month').annotate(num=Count('id')).order_by('-month').values('month', 'num')
    # print(blogs)
    html = ""

    for item in blogs:
        html += "<li><a href=\"\\?year={}&month={}\">{}({})</a></li>".format(item['month'].year, item['month'].month,item['month'].strftime('%Y-%m'), item['num'])
    # print(html)
    return mark_safe(html)

@register.simple_tag(name='read_rank')
def read_rank():
    # 分组查询
    # blogs = Blog.objects.filter().values('id', 'title')
    # blogs = Blog.objects.filter().order_by('-read_count').values('id', 'title', 'read_count')
    # print(blogs)
    html = ""
    conn = get_redis_connection("default")
    blogs = []
    for item in conn.zrange('read_count', 0, 5, desc=True):
        item = item.decode()
        blog_id, blog_title = item.split(":")
        read_count = int(conn.zscore('read_count', item))
        blogs.append(
            {
                "id":blog_id,
                "title":blog_title,
                "read_count":read_count
            }
        )
    for item in blogs:
        html += "<li><a href=\"\\article\\{}\">{}({})</a></li>".format(item['id'], item['title'][:10] + "..." if len(item['title']) > 10 else item['title'], item['read_count'])
    # print(html)
    return mark_safe(html)

