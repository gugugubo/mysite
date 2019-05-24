from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from read_statistic.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from django.utils import timezone
from django.core.cache import cache
from django.db.models import Sum
import datetime
from django.urls import reverse
from blog.models import Blog
from .forms import LoginForm, RegForm
from django.contrib.auth.models import User
from django.http import JsonResponse


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return blogs[:7]


def home(request):
    context = {}
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)

    blog_content_type = ContentType.objects.get_for_model(Blog)   # 传入Blog
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blogs_for_7_days'] = hot_blogs_for_7_days
    context['dates'] = dates
    context['read_nums'] = read_nums
    return render(request, 'home.html', context)

# LoginForm(request.POST)收到前端传回的form信息，并实例化一个对象

# 重定向 return redirect(request.GET.get('from'), reverse('home'))
# 提示错误 return render(request, 'error.html'）

#  authenticate() 来验证用户。它使用 username 和 password 作为参数来验证


def login(request):
    context = {}
    if request.method == 'POST':    # 判断是post还是get请求
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)               # 登录，需要一个request参数
            return redirect(request.GET.get('from'), reverse('home'))  # 重定向到原来的页面或首页
    else:
        # if a GET (or any other method) we'll create a blank form
        login_form = LoginForm()
    context['login_form'] = login_form
    return render(request, 'login.html', context)


def login_in(request):
    data = {}
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)               # 登录，需要一个request参数
        data['status'] = 'SUCCESS'
    else:
        data['error'] = 'ERROR'
    return JsonResponse(data)


def register(request):
    context = {}
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            password_again = reg_form.cleaned_data['password_again']
            user = User.objects.create_user(username, password, password_again)   # 注册用户
            user.save()
            auth.authenticate(username=username, password=password)       # 看看是否有改用户
            auth.login(request, user)                                    # 登录用户,需要request参数
            return redirect(request.GET.get('from'), reverse('home'))  # 重定向到首页
    else:
        # if a GET (or any other method) we'll create a blank form
        reg_form = RegForm()
    context['login_form'] = reg_form
    return render(request, 'login.html', context)
