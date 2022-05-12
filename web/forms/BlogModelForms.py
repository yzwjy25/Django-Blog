from django import  forms
from django.utils.safestring import mark_safe

from web.models import Blog



class MyContent(forms.Textarea):


    def render(self, name, value, attrs=None, renderer=None):
        print(name, value)

        html = """
        <div id="editor">
            <textarea style="display:none;" name={}>{}</textarea>
        </div>
        """.format(name, value if value else "")

        return mark_safe(html)


class BlogModelForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'category','content_sample', 'content', 'publish_time']

        widgets = {
            'title': forms.TextInput(attrs={"class":"form-control"}),
            "content": MyContent(),
            "category": forms.Select(attrs={"class":"form-control"})
        }
    class Media:
        # js = ('/static/admin/blog/createmarkdown.js', '/static/js/editormd.js')
        # css = ('/static/css/editormd.css', )
        pass