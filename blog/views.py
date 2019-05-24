from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count     # 计数的
from read_statistic.utils import read_statistics_once_read
from mysite.forms import LoginForm
# Create your views here.


def get_blog_list_common_date(request, blogs_all_list):
    context = {}
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)   # 分页
    page_num = request.GET.get('page', 1)    # 获取分页参数，没有的话默认给一个1
    page_of_blogs = paginator.get_page(page_num)  # 这是一个神奇的方法哦,能识别a和1
    # paginator.num_pages获取总页数
    # page_num是得到的页数
    # page_of_blogs.number显示当前页码
    # page_of_blogs.object_list该页所含的博客
    page_range = [x for x in range(int(page_num)-2, int(page_num)+3) if 0 < x <= paginator.num_pages]
    # 加上省略号
    if page_range[0]-1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context['page_range'] = page_range     # 显示的页数范围
    context['blogs'] = page_of_blogs.object_list   # 该页所含的博客
    context['pages_of_blogs'] = page_of_blogs       # 博客页面
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))   # 聚合函数，添加注释，BlogType将具有bolg_count属性
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    # Count里面是模型的小写 把这值保存到 blog_count 属性中
    context['blog_dates'] = Blog.objects.dates('create_time', 'month', order='DESC')
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_date(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)   # 返回了文章的key
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()     # 过滤大小
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()        # 前后页
    context['blog'] = blog
    context['login_form'] = LoginForm()
    # blog_content_type.model <class 'str'> 类型 跟字符串'blog'一样
    # initial初始化了字段content_type和object_id的值
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')   # response的set_cookies方法将cookies保存到浏览器,等关闭浏览器时cookies更新
    return response


def blog_with_type(request, blog_type_pk):
    blog_type = BlogType.objects.get(pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)

    context = get_blog_list_common_date(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blog_with_type.html', context)


def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)  # 过滤年份和月份

    context = get_blog_list_common_date(request, blogs_all_list)
    context['blog_with_date'] = '%s 年 %s 月' % (year, month)
    return render(request, 'blog/blogs_with_date.html', context)