# Django-Blog
基于Django简单的博客
## 环境
    Python3.6
    redis
## 运行启动
### 安装相关库
    pip install -r requirement.txt
### 更改Mysql和Redis配置
    在WebBlog的settings.py中找到并更改
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 数据库名,
            'USER': 账号,
            'PASSWORD': 密码,
            'HOST': '127.0.0.1',
            'PORT': 3306,
        }
    }
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
    在__init__中添加
    import pymysql
    pymysql.install_as_MySQLdb()
### 进行数据库迁移
    python manage.py makemigrations
    python manage.py migrate
### 启动
    python manage.py runserver 0.0.0.0:8080
    celery -A WebBlog.celery_tasks worker --loglevel=info -P eventlet --pool=solo
    Celery -A WebBlog.celery_tasks beat -l info
## 后台管理
    地址 http://localhost:8080/admin
    创建账号
    python manage.py createsuperuser
