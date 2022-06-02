from django.contrib.auth.models import AnonymousUser
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


@register.simple_tag
def userinfo(request):
    print(request.user)
    if isinstance(request.user, AnonymousUser):
        return mark_safe('<a href="/login/" class="btn" style="float: right;color: #fff;">登录</a>')

    html = '<a href="/logout/" class="btn" style="float: right;color: #fff;">注销</a><a href="#" class="btn" style="float: right;color: #fff;">{}</a>'.format(request.user.username)
    return mark_safe(html)