from .models import Likes, LikesDetail
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist

# Create your views here.


def likes(request):

    def error_response(code, message):
        data = {'code': code, 'status': 'ERROR', 'message': message}
        return JsonResponse(data)

    def success_response(like_num):
        data = {'status': 'SUCCESS', 'like_num': like_num}
        return JsonResponse(data)

    # 判断用户是否登录
    user = request.user
    if not user.is_authenticated:
        return error_response('400', '用户未登录')
    # 判断点赞对象是否存在try

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        blog = model_class.objects.get(id=object_id)
    except ObjectDoesNotExist:
        error_response(404, '未找到点赞对象')

    if request.GET.get('if_like') == 'true':    # 点赞
        # 判断用户是否点过赞
        likes_detail, created = LikesDetail.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        # 如果没点过赞，则返回true
        if created:
            like, created = Likes.objects.get_or_create(content_type=content_type, object_id=object_id)  # 为博客赞数加1
            like.num += 1
            like.save()
            return success_response(like.num)
        else:
            return error_response(402, '已点过赞')

    else:    # 取消点赞
        likes_detail, created = LikesDetail.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        # 用户点过赞，才能取消
        if not created:
            likes_detail.delete()
            unlike, created = Likes.objects.get_or_create(content_type=content_type, object_id=object_id)  # 为博客赞数减1
            if not created:
                unlike.num -= 1
                unlike.save()
                return success_response(unlike.num)
            else:
                return error_response(404, '取消点赞出错')
        else:
            return error_response(402, '取消出错')
