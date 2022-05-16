from django.core.paginator import Paginator


class MyPaginator(Paginator):
    def __init__(self, obj, current_page, per_page):
        super(MyPaginator, self).__init__(obj, per_page)
