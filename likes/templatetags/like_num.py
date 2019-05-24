from django import template
from ..models import Likes, LikesDetail

from django.contrib.contenttypes.models import ContentType
register = template.Library()


@register.simple_tag
def like_num(obj):
    content_type = ContentType.objects.get_for_model(obj)
    nums, created = Likes.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return nums.num


@register.simple_tag(takes_context=True)
def get_active(context, obj):
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    print('sdf')
    if not user.is_authenticated:
        return ''
    if LikesDetail.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''


@register.simple_tag
def get_model(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model



