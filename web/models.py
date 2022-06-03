from django.db import models


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=20, verbose_name="标题")

    content_sample = models.CharField(max_length=50, verbose_name="内容简介", null=True)

    content = models.TextField(verbose_name="内容")

    category = models.ForeignKey(to="Category", verbose_name='所属类别', on_delete=models.CASCADE, default=1)

    read_count = models.PositiveIntegerField(verbose_name='阅读数',default=0)

    publish_time = models.DateTimeField(verbose_name="发布时间")

    img = models.FileField(upload_to="static/blog_img/", default="static/blog_img/img.png")

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=10, verbose_name="类别")

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=20, verbose_name="发布者昵称")
    publish_time = models.DateTimeField(verbose_name="发布时间")
    content = models.TextField(verbose_name="内容")

    blog = models.ForeignKey(to='Blog', verbose_name='所属博客', on_delete=models.CASCADE, related_name='comment')

    def __str__(self):
        return f"{self.blog}:{self.name}:{self.content}"