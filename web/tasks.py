from WebBlog.celery_tasks import app
from .models import Blog
from django_redis import get_redis_connection
from django.core import mail
from django.conf import settings
import logging
import os, django


log = logging.getLogger("django")

@app.task(name='update_count')  # name表示设置任务的名称，如果不填写，则默认使用函数名做为任务名
def update_count():
    conn = get_redis_connection('default')
    blogs = []
    for item in conn.zrange('read_count', 0, -1):
        item = item.decode()
        blog_id = int(item.split(':')[0])
        blog = Blog.objects.filter(pk = blog_id).first()
        blog.read_count += conn.zscore('read_count', item)
        blogs.append(blog)
    conn.delete('read_count')
    Blog.objects.bulk_update(blogs, ['read_count'])

@app.task
def send_email_celery(**kwargs):

    mail.send_mail(
        subject='欢迎您注册',
        message='请点击下面链接激活您的账户:{}/{}/'.format(settings.SERVER_NAME + "/active",kwargs.get('csrfmiddlewaretoken')),
        from_email='1226856568@qq.com',
        recipient_list=[kwargs.get('email')]
    )

