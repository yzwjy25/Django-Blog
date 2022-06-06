import datetime
import json
import random

from django.conf import settings
# from django.contrib.auth.models import AnonymousUser
from django.contrib import auth
from django.db.models import Q, Count

from django.shortcuts import render, HttpResponse, redirect
from ratelimit.decorators import ratelimit

from .forms.UserForms import LoginForms, RegisterForms, UserInfo
from .service.Pager import MyPaginator
from .tasks import send_email_celery
from .models import Blog, Comment, Message
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
        Comment.objects.create(user_id=request.user.id, content=post_dict.get('editorContent'), blog_id=post_dict.get('articleid'), publish_time=datetime.datetime.now())
    return render(request, "web/read.html", {"blog":blog})


def message(request):
    if request.method == "POST":
        print(request.POST)
        editorContent = request.POST.get('editorContent')
        parentid = request.POST.get('parentid')
        targetMessageId = request.POST.get('targetMessageId')
        replyContent = request.POST.get('replyContent')
        if editorContent:
            Message.objects.create(user=request.user, content=editorContent, publish_time=datetime.datetime.now())
        else:
            Message.objects.create(
                user=request.user,
                content=replyContent,
                publish_time=datetime.datetime.now(),
                parent_id= parentid,
                reply_to_id=targetMessageId
            )

    messages = Message.objects.filter()
    msg_dict = {}
    for msg in messages:
        if not msg.parent:
            msg_dict[msg.id] = {
                "id": msg.id,
                "user": msg.user,
                "content": msg.content,
                "publish_time": msg.publish_time,
                "children" : []
            }
        else:
            msg_dict[msg.parent.id]['children'].append(
                {
                    "id": msg.id,
                    "user": msg.user,
                    "content": msg.content,
                    "publish_time": msg.publish_time,
                    "reply_to": msg.reply_to,
                }
            )


    print(msg_dict)

    return render(request, "web/message.html", {"msg_dict" : msg_dict})

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
        User = auth.get_user_model()
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
    # csrf_token = request.POST.get('csrfmiddlewaretoken')
    alphabet = 'abcdefghijklmnopqrstuvwxyz' + 'abcdefghijklmnopqrstuvwxyz'.upper()

    token = "".join(random.sample(alphabet, 15))
    if form.is_valid():
        send_email_celery.delay('欢迎您注册', '请点击下面链接激活您的账户:{}/{}/'.format(settings.SERVER_NAME + "/active", token), form.cleaned_data.get('email'))
        conn = get_redis_connection("default")
        conn.set(token, json.dumps(form.cleaned_data), 60)
        return render(request, "web/info.html", {"message":"验证信息已发送至邮箱，请前往邮箱查看。"})
    return render(request, "web/register.html", {"form": form})

def logout(request):
    auth.logout(request)
    return render(request, 'web/info.html', {"message":"您已退出登录。"})

# @ratelimit(key='ip', rate='1/30s', block=True, method="POST")
def forget(request, token=None):
    if not token:
        if request.method == 'GET':
            return render(request, 'web/forget.html', {"text":"邮箱"})
        alphabet = 'abcdefghijklmnopqrstuvwxyz' + 'abcdefghijklmnopqrstuvwxyz'.upper()

        token = "".join(random.sample(alphabet, 15))
        email = request.POST.get("text")
        send_email_celery.delay('找回密码', '请点击下面链接重置您的账户密码:{}/{}/'.format(settings.SERVER_NAME + "/forget",token), email)
        conn = get_redis_connection("default")
        conn.set(token, email, 60 * 5)
        return render(request, "web/info.html", {"message": "验证信息已发送至邮箱，请前往邮箱查看。有效期5分钟。"})
    if request.method == "GET":
        return render(request, 'web/forget.html', {"text":"密码"})
    try:
        conn = get_redis_connection("default")
        email = conn.get(token).decode()
        password = request.POST.get("text")
        # print(email, password)
        User = auth.get_user_model()
        user = User.objects.get(email=email)
        user.set_password(password)
        return render(request, 'web/info.html', {"message": "密码重置成功！"})
    except:
        return render(request, 'web/info.html', {"message": "密码重置失败！"})

def userinfo(request):
    if request.method == "GET":
        form = UserInfo()
        return render(request, "web/userinfo.html", {"form": form})
    form = UserInfo(files=request.FILES)
    if form.is_valid():
        print(form.cleaned_data)
        request.user.avatar = form.cleaned_data.get('avatar')
        print(request.user.avatar)
        request.user.save()
        return render(request, "web/info.html", {"message": "修改成功！"})
    return render(request, "web/userinfo.html", {"form": form})