from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.safestring import mark_safe

from web.service.myurl import withparam_url


class MyPaginator:
    def __init__(self,request, obj, per_page, current_page):

        paginator = Paginator(obj, per_page)
        try:
            pages = paginator.page(current_page)
            current_page = int(current_page)
        except PageNotAnInteger:
            current_page = 1
            pages = paginator.page(current_page)
        except EmptyPage:
            current_page = paginator.num_pages
            pages = paginator.page(current_page)

        #获取下一个和上一个页码
        if pages.has_next():
            next_page = pages.next_page_number()
        else:
            next_page = paginator.num_pages
        if pages.has_previous():
            pre_page = pages.previous_page_number()
        else:
            pre_page = 1
        self.current_page = current_page
        self.pre_page = pre_page
        self.next_page = next_page
        self.pages = pages
        self.request = request
        self.page_total = paginator.num_pages

    def page_html(self):
        page = ""
        for item in range(1, self.page_total + 1):
            page += f'<li class="{"active" if item==self.current_page else ""}"><a href="{withparam_url(self.request, "article", "page", item)}">{str(item)}</a></li>'
        html = f"""
        <nav aria-label="Page navigation" style="float: right;">
            <ul class="pagination pagination-sm">
                <li>
                    <a href="{withparam_url(self.request, "article", "page", self.pre_page)}" aria-label="Previous">
                        <span aria-hidden="true">«</span>
                    </a>
                </li>
        """ + page + f"""
                <li>
                    <a href="{withparam_url(self.request, "article", "page", self.next_page)}" aria-label="Next">
                        <span aria-hidden="true">»</span>
                    </a>
                </li>
            </ul>
        </nav>
        """
        return mark_safe(html)