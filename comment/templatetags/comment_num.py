from django import template
from ..models import Comment
from ..forms import CommentForm
from django.contrib.contenttypes.models import ContentType
register = template.Library()


@register.simple_tag
def comment_nums(obj):      # 得到评论数
    content_type = ContentType.objects.get_for_model(obj)
    num = Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()
    return num


@register.simple_tag
def get_comment(obj):           # 得到评论
    content_type = ContentType.objects.get_for_model(obj)   # 得到content_type类型
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)  # 得到文章的评论
    return comments.order_by('-comment_time')


@register.simple_tag
def comment_form(obj):      # 得到form表单
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(
        initial={'content_type': content_type.model,
                 'object_id': obj.pk,
                 'reply_comment_id': 0})         # 将触发验证，HTML输出将包括任何验证错误：
    return form
