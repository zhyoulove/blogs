from django import forms
from .models import BlogCategory  # 如果你有 BlogCategory 模型
from .models import BlogComment  # 导入 BlogComment 模型


"""
    这个地方主要是针对前端表单进行验证
"""
class PubBlogForm(forms.Form):
    title = forms.CharField(max_length=120, label="博客标题")
    content = forms.CharField(widget=forms.Textarea, label="博客内容")  # 使用 Textarea widget 来处理富文本内容
    category = forms.ModelChoiceField(queryset=BlogCategory.objects.all(), label="选择分类")





class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']  # 只包含评论内容字段
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入您的评论', 'rows': 3}),
        }
