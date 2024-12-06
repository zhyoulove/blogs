from .models import BlogCategory, Blog, BlogComment
from django.contrib import admin
# Register your models here.
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'category' , 'author' , 'pub_time']


# 博客评论
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['blog' , 'content', 'author', 'pub_time']


# 进行注册
admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)