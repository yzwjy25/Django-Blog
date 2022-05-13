import datetime
import json

from django.shortcuts import render, HttpResponse
from .models import Blog

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

    return render(
        request,
        "web/index.html",
        {
            "articles":article,
            'search_value':value
        }
    )

def blogcontent(request, blog_id):
    blog = Blog.objects.filter(pk = blog_id).first()
    readed_list = json.loads(request.COOKIES.get('readed', '[]'))
    # print(readed_list, type(readed_list))

    response = render(request, "web/content.html", {"blog": blog})

    if blog.id not in readed_list:
        print(readed_list)
        blog.increase_views()
        readed_list.append(blog.id)
        response.set_cookie('readed', readed_list)


    return response