from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistic.models import ReadNumExpandMethod
from read_statistic.models import ReadNum, ReadDetail
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):      # <Question: Question object (1)> 在后台管理界面可以看到返回的内容
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=50)
    read_details = GenericRelation(ReadDetail)
    content = RichTextUploadingField()
    create_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:     # 这个字段是告诉Django模型对象返回的记录结果集是按照哪个字段排序的。
        ordering = ['-create_time']
