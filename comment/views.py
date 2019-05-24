from .models import Comment
from .forms import CommentForm
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
# Create your views here.

#  reverse 避免了我们在视图函数中硬编码URL


def update_comment(request):
    data = {}   # create a form instance and populate it with data from the request:
    comment_form = CommentForm(request.POST, user=request.user)         # 实例化到我们希望发布的URL的对应的视图
    # check whether it's valid:
    if comment_form.is_valid():
        # 检查通过，保存数据
        comment = Comment()  # 实例化一条评论
        comment.user = request.user
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if parent:   # 这是一条回复
            comment.parent = parent     # 父评论
            comment.reply_to = parent.user  # 父评论用户
            comment.root = parent.root if parent.root else parent
        comment.save()

        # 返回数据，评论内容，评论者，评论对象，评论时间
        data['status'] = 'SUCCESS'
        data['text'] = comment.text
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['pk'] = comment.pk
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if parent:
            data['reply_to'] = comment.reply_to.username        # 传回回复评论的用户
        else:
            data['reply_to'] = ''

        data['root_pk'] = comment.root.pk if comment.root else ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]    # 提示错误信息
    return JsonResponse(data)   # 返回json数据
