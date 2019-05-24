from django.contrib import admin
from .models import LikesDetail, Likes
# Register your models here.


@admin.register(LikesDetail)
class LikesDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_time', 'object_id', 'content_object')


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'num', 'content_object')

