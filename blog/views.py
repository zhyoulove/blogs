from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, reverse, get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods , require_GET
from .models import *
from .forms import *
from django.http.response import JsonResponse


# Create your views here.
def index(request):
    # 查询所有博客，并进行展示
    blogs = Blog.objects.all()
    return render(request, "index.html", {"blogs": blogs})


@login_required
def blog_detail(request, blog_id):
    # 获取博客对象
    blog = get_object_or_404(Blog, id=blog_id)

    # 获取博客下的所有评论
    comments = BlogComment.objects.filter(blog=blog).order_by('-pub_time')

    # 如果是 POST 请求，说明用户提交了评论
    if request.method == 'POST':
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            # 创建并保存评论
            new_comment = form.save(commit=False)
            new_comment.blog = blog  # 设置关联的博客
            new_comment.author = request.user  # 设置评论作者为当前登录的用户
            new_comment.save()  # 保存评论

            # 提交成功后重定向到当前页面，以显示新评论
            return redirect('detail', blog_id=blog.id)
    else:
        form = BlogCommentForm()

    return render(request, "blog_detail.html", {
        "blog": blog,
        "comments": comments,
        "form": form
    })


"""
    需要先进行登录，才可以跳转到发布博客这个页面
"""


@require_http_methods(["GET", "POST"])
@login_required
def blog_pub(request):
    if request.method == "GET":
        categorys = BlogCategory.objects.all()
        return render(request, "blog_pub.html", {"categorys": categorys})
    else:
        # 表示进行表单的提交
        form = PubBlogForm(request.POST)
        # print(form)
        if form.is_valid():  # 表示表单的数据都符合要求
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            category_id = form.cleaned_data["category"].id
            print(category_id, type(category_id))
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            return JsonResponse({"code": 200, "message": "博客发布成功！" , "blog_id":blog.id})
        else:
            return JsonResponse({"code": 400, "message": "参数错误！"})


@require_GET
def search(request):
    # 因为这块前端是通过get请求传过来的参数，所有通过下面这个方式进行获取
    q = request.GET.get("q")
    print(f"获取的参数为：{q}")
    # 获取标题和博客内容中都含有q的blogs Q表达式含有或的意思
    blogs = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))

    return render(request, "index.html", {"blogs": blogs})
