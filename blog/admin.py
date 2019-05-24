from django.contrib import admin
from .models import Blog, BlogType

# Register your models here.


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')   # 展示的信息


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blog_type', 'get_read_num', 'author', 'create_time', 'last_updated_time')






