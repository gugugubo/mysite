from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# Create your models here.

# ContentType,包含全部模型
# model_class 返回此ContentType实例表示的模型类


class Comment(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    # 储存id号
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')     # 并不会在数据库生成对应字段

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.DO_NOTHING)
    # 记录老祖宗评论
    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.DO_NOTHING)
    # 记父评论
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.DO_NOTHING)
    # 记录父评论的用户是谁
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-comment_time']

