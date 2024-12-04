$(document).ready(function () {
    $('#loginForm').on('submit', function (e) {
        e.preventDefault();  // 阻止默认的表单提交行为

        // 清空消息区域
        $('#message').hide();
        $('#message-list').empty();

        // 获取表单数据
        var email = $('#email').val();
        var password = $('#password').val();
        var rememberMe = $('#rememberMe').is(':checked') ? 1 : 0;

        // 发送 AJAX 请求
        $.ajax({
            url: '/auths/user_login',  // 替换为登录的处理 URL，如果需要
            method: 'POST',
            data: {
                'email': email,
                'password': password,
                'rememberme': rememberMe,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                // 处理服务器返回的成功信息
                if (response.success) {
                    // 登录成功，跳转到首页或其他页面
                    window.location.href = response.redirect_url || '/';
                } else {
                    // 显示错误信息
                    $('#message').show();
                    $('#message-list').append('<li>' + response.error_message + '</li>');
                }
            },
            error: function () {
                // 如果请求失败，显示一个通用错误信息
                $('#message').show();
                $('#message-list').append('<li>服务器错误，请稍后重试。</li>');
            }
        });
    });
});
