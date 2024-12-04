from auths.forms import RegisterForm
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render , redirect , reverse
import string
import random
from django.core.mail import send_mail
import redis
from django_redis import get_redis_connection
from django.conf import settings
import time
from django.views.decorators.http import require_http_methods
from .forms import LoginForm
from django.contrib.auth import get_user_model , login
# Create your views here.

User =get_user_model()

@require_http_methods(['GET', 'POST'])
def user_register(request):
    if request.method == 'GET':
        return render(request, 'user_register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('auths:user_login'))

        else:
            return render(request, 'user_register.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def user_login(request):
    if request.method == 'GET':
        return render(request, 'user_login.html')
    else:
        # 这个地方首先需要验证输入的表单是否合法
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            rememberme = form.cleaned_data['rememberme']
            user = User.objects.filter(email=email).first()

            print(rememberme , type(rememberme))
            # 如果用户存在，并且密码正确，进行登录逻辑
            if user and user.check_password(password):
                # 登录
                login(request, user)
                # 在判断是否需要记住我
                if not rememberme:
                    # print("我触发了哦！！！！")
                    # 表示没有点击记住我，那么设置session过期时间为本次会话
                    request.session.set_expiry(0)
                # 如果点击了，默认就是两周的过期时间
                return redirect(reverse('index'))
            else:
                return render(request, 'user_login.html', {'form': "邮箱或者密码错误！"})







# 发送注册邮箱验证码
# xxx ?email=xxx
def send_email(request):
    email = request.GET.get('email')
    # print(email)
    # 如果邮箱为空，表示需要传递邮箱这个参数
    if email is None:
        return JsonResponse({"code":400 , "message":"必须传递邮箱！"})


    # 表示获取到了需要发送的邮箱 先随机生成四位数字
    code = "".join(random.sample(string.digits , 6))
    print(code)
    # 进行发送
    send_mail("注册博客验证码" , message=f'您的注册验证码是：{code}' , recipient_list=[email] , from_email=None)

    """将验证码保存到 Redis，设置过期时间"""
    redis_conn = get_redis_connection("default")  # 获取 Redis 连接

    # 存储验证码，并设置过期时间（如 5 分钟）
    redis_conn.setex(email, settings.REDIS_TIMEOUT, code)  # 使用邮箱作为键

    return JsonResponse({"code":200 , "message":"邮箱验证码发送成功！"})
