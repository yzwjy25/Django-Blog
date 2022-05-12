import datetime

from django.shortcuts import render, HttpResponse
from .models import Blog
import markdown
# Create your views here.
def index(request):
    article = Blog.objects.filter().order_by('-publish_time').values("id", "title","content_sample", "publish_time")

    return render(
        request,
        "web/index.html",
        {
            "articles":article
        }
    )

def blogcontent(request, blog_id):
    blog = Blog.objects.filter(pk = blog_id).first()

    return render(request, "web/content.html", {"blog":blog})