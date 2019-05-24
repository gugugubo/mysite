from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Comment


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)  # widget设置了它不显示 错误信息键：required，max_length，min_length
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'), error_messages={'request': '评论内容不为空'})  #这是一个自定义错误消息：
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))  # 记录回复对象，并设置id值
    # CommentForm(initial={'content_type': blog_content_type.model, 'object_id': blog_pk}) 初始化html的值，即规定value值
    # 实例化时初始化会直接验证值是否正确
    #  initial values are not used as “fallback” data in validation if a particular field’s value is not given.
    # initial values are only intended for initial form display:

    def __init__(self, *args, **kwargs):   # 将验证步骤都放在form中
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:              # 评论对象验证
            self.cleaned_data['user'] = self.user       # 返回user
        else:
            raise forms.ValidationError('尚未登录')

        # 验证评论对象是否存在
        content_type = self.cleaned_data['content_type']
        object_id = int(self.cleaned_data['object_id'])
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')

        return self.cleaned_data

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError('回复出错')
        elif reply_comment_id == 0:         # 这是一条评论不是回复
            self.cleaned_data['parent'] = None      # 所以没有父对象
        elif Comment.objects.filter(pk=reply_comment_id).exists():    # 找到父评论
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError('回复出错')
        return reply_comment_id
