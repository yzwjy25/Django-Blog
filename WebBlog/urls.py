"""WebBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from web.views import index, detial, login, register, active, logout, article, message, forget, userinfo



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('index/', index, name="index"),
    path('article/', article, name="article"),
    path('article/<int:blog_id>/', detial, name="detial"),
    path('message/', message, name="message"),
    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path('active/<str:id_>/', active, name="active"),
    path('logout/', logout, name="logout"),
    path('forget/', forget, name='forget'),
    path('forget/<str:token>/', forget, name='forget_token'),
    path('userinfo/', userinfo, name='userinfo'),
]
