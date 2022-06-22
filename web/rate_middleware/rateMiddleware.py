import json
import time
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection


class RateMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print(request.path, request.method)
        path = ['/register/', '/forget/']
        if request.path not in path or request.method != 'POST':
            return
        conn = get_redis_connection('default')
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get("HTTP_X_FORWARDED_FOR")
        else:
            ip = request.META.get("REMOTE_ADDR")
        print(ip)
        last_visit_time = conn.hget('rate_limit', ip)
        # print(visit_list)
        if not last_visit_time:
            conn.hset("rate_limit", ip, time.time())
            return

        last_visit_time = float(last_visit_time.decode())
        now_time = time.time()

        if now_time - 60 <= last_visit_time:
            return render(request, "web/info.html", {"message": f"访问太频繁，请{int(60 - now_time + last_visit_time)}秒后再试！"})
        conn.hset("rate_limit", ip, now_time)