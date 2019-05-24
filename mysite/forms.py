from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
# auth.authenticate验证用户名密码
# user.is_authenticated 验证是否登录
# auth..models.User  User.objects.filter(username=username).exists() 验证用户信息
# User.objects.create_user(username, password, password_again)  新建用户
# request.user 得到登录用户

# 新建两个字段， label设置了对应的label标签 min_length 或max_length，widget设置他的type,class属性

# clean_字段名，自动验证信息，用self.cleaned_data['']取出信息


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):     # 自动验证信息
        username = self.cleaned_data['username']  # 取出信息
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)  # 尝试登录验证
        if user is None:
            raise forms.ValidationError("用户名或密码不正确")   # 验证失败报错
        else:                                           # 验证成功
            self.cleaned_data['user'] = user   # 传回user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=10,
        min_length=3,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入3-10位的用户名'}
        )
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}
        )
    )
    password = forms.CharField(
        label='用户名',
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入密码(最少6位)'}
        )
    )
    password_again = forms.CharField(
        label='用户名',
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入3-10位的用户名'}
        )
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password_again = self.cleaned_data['password_again']
        password = self.cleaned_data['password']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again




