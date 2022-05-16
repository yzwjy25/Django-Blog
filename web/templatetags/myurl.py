from django.http import QueryDict
from django.template import Library
from django.urls import reverse

register = Library()

@register.simple_tag(name='memory_url')
def memory_url(request, name, *args, **kwargs):
    basic_url = reverse(name, args=args, kwargs=kwargs)
    if not request.GET:
        return basic_url

    old_params = request.GET.urlencode()
    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = old_params

    return '%s?%s' % (basic_url, query_dict.urlencode())

@register.simple_tag(name='withparam_url')
def withparam_url(request, name,  key, value):
    # print(":::::::", name)
    basic_url = reverse(name)
    if not request.GET:
        url = basic_url + "?{}={}".format(key, value)
    else:
        d = request.GET.dict()
        d[key] = value
        con = '&'.join(["{}={}".format(k, v) for k,v in d.items()])
        url = basic_url + "?{}".format(con)
    return url