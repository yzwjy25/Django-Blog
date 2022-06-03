import datetime
import json
from django.contrib.auth.models import User, AnonymousUser
from django.contrib import auth
from django.db.models import Q, Count

from django.shortcuts import render, HttpResponse, redirect
from ratelimit.decorators import ratelimit

from .forms.UserForms import LoginForms, RegisterForms
from .service.Pager import MyPaginator
from .tasks import send_email_celery
from .models import Blog, Comment
from django_redis import get_redis_connection
# Create your views here.


def index(request):
    return render(request, 'web/index.html')

def article(request):
    query_con = {}
    category_id = request.GET.get('category')
    content = request.GET.get('content')
    if category_id:
        query_con['category_id'] = category_id
    if content:
        query_con["content__icontains"] = content
    blog = Blog.objects.filter(**query_con).annotate(c = Count("comment")).values("id", "title", "content_sample", "category__title", "read_count", "publish_time", "c", 'img')
    current_page = request.GET.get("page")
    Page = MyPaginator(request, blog, 7, current_page)
    return render(request, 'web/article.html', {"Page":Page})

def detial(request, blog_id):
    blog = Blog.objects.filter(pk=blog_id).first()
    conn = get_redis_connection("default")
    conn.zincrby('read_count', 1.0, "{}:{}".format(blog.id, blog.title))
    if request.method == "POST":
        if not request.user.username:
            return render(request, "web/info.html", {"message":"您未登录，请先登录。"})
        post_dict = request.POST.dict()
        Comment.objects.create(name=request.user.username, content=post_dict.get('editorContent'), blog_id=post_dict.get('articleid'), publish_time=datetime.datetime.now())
    return render(request, "web/read.html", {"blog":blog})


def message(request):
    return render(request, "web/message.html")

def login(request):

    if request.method == "GET":
        form = LoginForms()
        return render(request, 'web/login.html', {"form":form})
    form = LoginForms(data=request.POST)
    if form.is_valid():
        # print()
        user = auth.authenticate(**form.cleaned_data)
        if user:
            auth.login(request, user)
            return redirect("article")
        else:
            return render(request, 'web/login.html', {"error": "账号或密码错误！", "form":form})
    return render(request, 'web/login.html', {"form": form})

def active(request, id_):
    try:
        conn = get_redis_connection("default")
        msg = json.loads(conn.get(id_).decode())
        # print(msg)
        msg.pop('repassword')
        User.objects.create_user(**msg)
        return render(request, "web/info.html", {"message": "验证成功！前往<a href=\"/login/\">登录</a>"})
    except:
        return render(request, "web/info.html", {"message": "验证失败，请重新再试！"})
    # return render(request, "web/info.html", {"message": "验证成功！前往<a href=\"/login/\">登录</a>"})

@ratelimit(key='ip', rate='1/30s', block=True, method="POST")
def register(request):
    if request.method == "GET":
        form = RegisterForms()
        return render(request, "web/register.html", {"form": form})
    form = RegisterForms(data=request.POST)
    csrf_token = request.POST.get('csrfmiddlewaretoken')
    if form.is_valid():
        send_email_celery.delay(csrf_token, form.cleaned_data.get('email'))
        conn = get_redis_connection("default")
        conn.set(csrf_token, json.dumps(form.cleaned_data), 60)
        return render(request, "web/info.html", {"message":"验证信息已发送至邮箱，请前往邮箱查看。"})
    return render(request, "web/register.html", {"form": form})

def logout(request):
    auth.logout(request)
    return render(request, 'web/info.html', {"message":"您已退出登录。"})