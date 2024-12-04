from django import forms
from django.contrib.auth import get_user_model

# redis中需要
from django_redis import get_redis_connection


User = get_user_model()
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20 , min_length = 2 , error_messages={
        'required':'请传入用户名!',
        'max_length':'用户名长度应在2 - 20 之间！',
        'min_length':'用户名长度应在2 - 20 之间！'
    })
    email = forms.EmailField(error_messages={
        'required':'请输入邮箱！',
        'invalid':'请输入正确的邮箱！'
    })
    captcha = forms.CharField(max_length = 6, min_length = 6)
    password = forms.CharField(max_length = 20, min_length = 6)


    def clean_email(self):
        email = self.cleaned_data['email']
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError("该邮箱已经被注册")
        return email

    def clean_captcha(self):
        # 得到提交的验证码
        captcha = self.cleaned_data['captcha']
        email = self.cleaned_data['email']
        redis_conn = get_redis_connection("default")  # 获取 Redis 连接
        # 获取 Redis 中存储的验证码
        value = redis_conn.get(email)
        str_value = value.decode('utf-8')
        if str_value == captcha:
            print("验证码正确了！")
            # 删除 Redis 中存储的验证码
            redis_conn.delete(email)
            return captcha
        else:
            raise forms.ValidationError("邮箱或验证码错误!")



class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={
        'required': '请输入邮箱！',
        'invalid': '请输入正确的邮箱！'
    })
    password = forms.CharField(max_length=20, min_length=2)
    # 可选择的
    rememberme = forms.CharField(required=False)


