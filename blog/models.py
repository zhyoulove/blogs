from django.db import models
from django.contrib.auth import get_user_model

# 获取当前项目中的用户模型
User = get_user_model()

"""
    分类表
"""
class BlogCategory(models.Model):
    name = models.CharField(max_length=200 , verbose_name='分类名称')


    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "博客分类"
        verbose_name_plural = verbose_name


"""
    博客模型
"""
class Blog(models.Model):
    title = models.CharField(max_length=200 , verbose_name='博客标题')
    content = models.TextField(verbose_name="博客内容")
    pub_time = models.DateTimeField(auto_now_add=True , verbose_name='发布时间')
    # 表示每一个博客都对应一个分类：BlogCategory 被删除时，所有与该分类相关联的 Blog 实例也会被删除
    # 换句话说，如果删除某个分类，所有属于该分类的博客会被一起删除。
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE , verbose_name='所属分类')
    author = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name='发布作者')

    def __str__(self):
        return self.title

    def get_excerpt(self, length=100):
        """ 获取博客内容的前部分作为简介 """
        return self.content[:length] + ('...' if len(self.content) > length else '')
    class Meta:
        verbose_name = '博客列表'
        verbose_name_plural = verbose_name

"""
    评论模型
"""
class BlogComment(models.Model):
    content = models.TextField(verbose_name="评论内容")
    pub_time = models.DateTimeField(auto_now_add=True , verbose_name='评论时间')
    # 每一个评论都应该在博客下，当博客被删除时，这条博客下的所有评论都应该被删除
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE , verbose_name='评论博客')

    # 用户：评论   一对多  ， 用户被删除时，该用户所有的评论都被删除
    author = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name='评论人')

    def __str__(self):
        return self.content
    class Meta:
        verbose_name = '博客评论'
        verbose_name_plural = verbose_name