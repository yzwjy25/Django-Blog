import datetime
import json
from django.contrib.auth.models import User, AnonymousUser
from django.contrib import auth
from django.core import mail
from django.db.models import Q

from django.shortcuts import render, HttpResponse, redirect
from .tasks import send_email_celery
from .models import Blog, Comment
from django_redis import get_redis_connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def index(request):

    query_con = {}
    #按条件查询
    category_id = request.GET.get('category')
    year = request.GET.get('year')
    month = request.GET.get('month')

    if category_id:
        query_con['category_id'] = category_id
    if year and month:
        query_con['publish_time__year'] = year
        query_con['publish_time__month'] = month
    #搜索

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
    #分页处理
    current_page = request.GET.get("page")
    paginator = Paginator(article, 5)
    try:
        pages = paginator.page(current_page)
        current_page = int(current_page)
    except PageNotAnInteger:
        current_page = 1
        pages = paginator.page(current_page)
    except EmptyPage:
        current_page = paginator.num_pages
        pages = paginator.page(current_page)

    #获取下一个和上一个页码
    if pages.has_next():
        next_page = pages.next_page_number()
    else:
        next_page = paginator.num_pages
    if pages.has_previous():
        pre_page = pages.previous_page_number()
    else:
        pre_page = 1

    return render(
        request,
        "web/index.html",
        {
            "articles":pages,
            'search_value':value,
            "next_page":next_page,
            "pre_page":pre_page,
            "page_range":paginator.page_range,
            "current_page":current_page
        }
    )


def blogcontent(request, blog_id):
    blog = Blog.objects.filter(pk = blog_id).first()
    readed_list = json.loads(request.COOKIES.get('readed', '[]'))
    if request.method == 'POST':
        print(request.POST)
        content = request.POST.get('content')
        # if request.user
        if isinstance(request.user, AnonymousUser):
            return HttpResponse("请先登录！")
        Comment.objects.create(name=request.user.username, publish_time=datetime.datetime.now(), content=content, blog_id=blog_id)


    conn = get_redis_connection("default")
    response = render(request, "web/content.html", {"blog": blog})
    # print(blog.comment)
    if blog.id not in readed_list:
        # print(conn.zscore('read_count', "{}:{}".format(blog.id, blog.title)))
        # read_count = conn.incr("article:{}".format(blog.id))
        # print(read_count)
        conn.zincrby('read_count', 1.0, "{}:{}".format(blog.id, blog.title))
        # conn.zadd('read_count', {"{}:{}".format(blog.id, blog.title): 1})
        # blog.increase_views()
        readed_list.append(blog.id)
        response.set_cookie('readed', readed_list, )

    return response


def login(request):
    if request.method == "GET":
        return render(request, 'web/login.html')
    d = request.POST.dict()
    d.pop('csrfmiddlewaretoken')
    user = auth.authenticate(**d)
    if user:
        auth.login(request, user)
        return redirect("index")
    return render(request, 'web/login.html')

def active(request, id_):
    # r = send_email_celery.delay("1226856568@qq.com")
    # print(r)
    conn = get_redis_connection("default")
    msg = json.loads(conn.get(id_).decode())
    User.objects.create_user(**msg)
    return redirect('login')

def register(request):
    if request.method == "GET":
        return render(request, "web/register.html")
    d = request.POST.dict()
    if User.objects.filter(Q(username=d.get('username')) | Q(email=d.get('email'))).exists():
        return HttpResponse('账号或者邮箱已存在，请重新输入')
    send_email_celery.delay(**d)
    conn = get_redis_connection("default")
    conn.set(d.pop('csrfmiddlewaretoken'), json.dumps(d), 60)

    return HttpResponse('验证码已发送至邮箱，请注意查收')

def logout(request):
    auth.logout(request)
    return redirect("index")