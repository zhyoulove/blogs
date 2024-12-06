$(document).ready(function () {
    // 当提交表单时，将富文本编辑器的内容保存到隐藏字段中
    $("#blog-form").submit(function (event) {
        event.preventDefault();  // 阻止默认表单提交

        // 获取富文本编辑器的内容
        var content = quill.root.innerHTML;
        $("#content").val(content);  // 将内容放入隐藏的输入框中
        // 使用AJAX提交表单数据
        $.ajax({
            url: '',  // 当前页面URL
            type: 'POST',
            data: $(this).serialize(),  // 序列化表单数据
            success: function (response) {
                if (response.code == 200) {
                    alert(response.message);  // 显示成功消息
                    // 可以在这里进行页面跳转或者清空表单等操作
                } else {
                    alert(response.message);  // 显示错误消息
                }
            },
            error: function (xhr, status, error) {
                alert('发布失败，请重试！');
            }
        });
    });
}