from django.db import models


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=20, verbose_name="标题")

    content_sample = models.CharField(max_length=50, verbose_name="内容简介", null=True)

    content = models.TextField(verbose_name="内容")

    category = models.ForeignKey(to="Category", verbose_name='所属类别', on_delete=models.CASCADE, default=1)

    read_count = models.PositiveIntegerField(verbose_name='阅读数',default=0)

    def increase_views(self):
        self.read_count += 1
        self.save(update_fields=['read_count'])

    publish_time = models.DateTimeField(verbose_name="发布时间")

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=10, verbose_name="类别")

    def __str__(self):
        return self.title
