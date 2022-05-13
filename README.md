# Django-Blog
基于Django简单的博客
## 环境
    Python3.6
## 运行启动
### 安装相关库
    pip install -r requirement.txt
### 更改数据库配置
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
### 进行数据库迁移
    python manage.py makemigrations
    python manage.py migrate
### 启动
    python manage.py runserver 0.0.0.0:8080
## 后台管理
    地址 http://localhost:8080/admin
	创建账号
	python manage.py createsuperuser
