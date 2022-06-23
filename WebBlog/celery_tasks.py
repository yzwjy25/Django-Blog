from __future__ import absolute_import, unicode_literals

import datetime
import os
from celery import Celery

# 设置环境变量
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebBlog.settings')

# 注册Celery的APP
app = Celery('mydjango')
# 绑定配置文件
app.config_from_object("WebBlog.config")

# 自动发现各个app下的tasks.py文件
app.autodiscover_tasks(['web'])
app.conf.beat_schedule = {
    "test_task": {
        "task": "update_count",
        "schedule": crontab(minute=0, hour=0), #每天零点更新数据库
    }
}
