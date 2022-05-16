import datetime
import json

from django.shortcuts import render, HttpResponse
from .models import Blog
from django_redis import get_redis_connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from .service.pager import MyPaginator


def index(request):

    query_con = {}
    #按条件查询
    category_id = request.GET.get('category')
    year = request.GET.get('year')
    month = request.GET.get('month')
    current_page = request.GET.get("page")
    if category_id:
        query_con['category_id'] = category_id
    if year and month:
        query_con['publish_time__year'] = year
        query_con['publish_time__month'] = month
    #搜索
    if not current_page:
        current_page = 1
    value = ''
    if request.method == 'POST':
        type_ = request.POST.get('type')
        value = request.POST.get('value')
        # print(type_, value)
        if type_ == 'title':
            query_con['title__contains'] = value
        else:
            query_con['content__contains'] = value

    article = Blog.objects.filter(**query_con).order_by('-publish_time').values("id", "title","content_sample", "publish_time")
    paginator = MyPaginator(article, current_page, 2)
    print(paginator.num_pages)
    try:
        pages = paginator.page(current_page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    print(pages)
    # print(pages.next_page_number())

    return render(
        request,
        "web/index.html",
        {
            "articles":pages,
            'search_value':value
        }
    )

def blogcontent(request, blog_id):
    blog = Blog.objects.filter(pk = blog_id).first()
    readed_list = json.loads(request.COOKIES.get('readed', '[]'))
    # print(readed_list, type(readed_list))

    conn = get_redis_connection("default")
    response = render(request, "web/content.html", {"blog": blog})

    if blog.id not in readed_list:
        read_count = conn.incr("article:{}".format(blog.id))
        print(read_count)
        conn.zadd('read_count', {"article:{}".format(blog.id): 1})
        # blog.increase_views()
        readed_list.append(blog.id)
        response.set_cookie('readed', readed_list)
    return response