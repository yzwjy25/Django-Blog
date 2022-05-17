from django import  forms

from web.models import Comment


class CommentModelForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['publish_time', 'blog']
