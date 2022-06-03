import datetime
from lxml import etree
import markdown
from django.contrib import admin
from django.shortcuts import render, redirect

from .models import Blog, Category, Comment
from .forms.BlogModelForms import BlogModelForm

# from django.forms import TextInput
# Register your models here.
admin.site.site_header = '博客后台系统'
admin.site.site_title = '博客后台'



class BlogModelAdmin(admin.ModelAdmin):
    form = BlogModelForm
    list_display = ('title', 'content_sample', 'category', 'publish_time')
    change_form_template = 'madmin/blog_change.html'

admin.site.register(Category)
admin.site.register(Blog, BlogModelAdmin)
admin.site.register(Comment)

# admin
