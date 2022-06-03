from django.urls import reverse


def withparam_url(request, name,  key, value):
    basic_url = reverse(name)
    if not request.GET:
        url = basic_url + "?{}={}".format(key, value)
    else:
        d = request.GET.dict()
        d[key] = value
        con = '&'.join(["{}={}".format(k, v) for k,v in d.items()])
        url = basic_url + "?{}".format(con)
    return url
