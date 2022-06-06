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
        blog = Blog.objects.filter(pk=blog_id).first()
        blog.read_count += conn.zscore('read_count', item)
        blogs.append(blog)
    conn.delete('read_count')
    Blog.objects.bulk_update(blogs, ['read_count'])


@app.task
def send_email_celery(subject, message, email):
    mail.send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )

# @app.task
# def forget_password(csrftoken, email):
#
#     mail.send_mail(
#         subject='找回密码',
#         message='请点击下面链接重置您的账户密码:{}/{}/'.format(settings.SERVER_NAME + "/forget",csrftoken),
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[email]
#     )
