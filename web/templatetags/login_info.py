from django.contrib.auth.models import AnonymousUser
from django.template import Library
from django.urls import reverse
from django.utils.safestring import mark_safe

register = Library()


@register.simple_tag
def userinfo(request):
    # print(request.user)
    if isinstance(request.user, AnonymousUser):
        return mark_safe('<a href="/login/" class="blog-user" style="font-size:15px;"><i class="fa fa-user"> 未登录</i></a>')
    html = f'<span class="blog-user" style="font-size:15px;">{request.user.username} <a href="{reverse("logout")}"><i class="fa fa-power-off"></i></a></span>'
    return mark_safe(html)