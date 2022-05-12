import datetime

from django.shortcuts import render, HttpResponse
from .models import Blog

# Create your views here.
def index(request):
    query_con = {}
    category_id = request.GET.get('category')
    year = request.GET.get('year')
    month = request.GET.get('month')
    if category_id:
        query_con['category_id'] = category_id
    if year and month:
        query_con['publish_time__year'] = year
        query_con['publish_time__month'] = month
    article = Blog.objects.filter(**query_con).order_by('-publish_time').values("id", "title","content_sample", "publish_time")

    return render(
        request,
        "web/index.html",
        {
            "articles":article
        }
    )

def blogcontent(request, blog_id):
    blog = Blog.objects.filter(pk = blog_id).first()
    blog.read_count += 1
    blog.save()
    return render(request, "web/content.html", {"blog":blog})