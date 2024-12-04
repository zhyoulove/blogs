$(document).ready(function () {
    // 定义倒计时时间
    var countdownTime = 10;  // 60秒倒计时
    var timer;  // 定时器

    // 发送验证码按钮点击事件
    $("#sendCaptcha").click(function () {
        // 获取邮箱输入框的值
        var email = $("#email").val().trim();

        // 判断邮箱是否为空
        if (!email) {
            alert("请输入邮箱！");
            return;
        }

        // 正则表达式验证邮箱格式
        var emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        if (!emailPattern.test(email)) {
            alert("请输入有效的邮箱地址！");
            return;
        }

        // 禁用发送验证码按钮，并显示倒计时
        $(this).prop("disabled", true);
        $(this).text(countdownTime + "秒");

        // 开始倒计时
        startCountdown();

         $.ajax('/auths/send_email?email='+email , {
            method : 'GET',
            success : function (result) {
                if(result['code'] == 200){
                    alert("验证码发送成功！")
                }else {
                    alert(result['message'])
                }
            },
            fail: function (error){
                console.log(error)
            }
        })


    });

    // 倒计时函数
    function startCountdown() {
        // 每秒更新倒计时
        timer = setInterval(function () {
            countdownTime--;  // 倒计时减1
            $("#sendCaptcha").text(countdownTime + "秒");  // 更新按钮上的倒计时文本

            // 当倒计时结束，恢复按钮可点击状态
            if (countdownTime <= 0) {
                clearInterval(timer);  // 停止定时器
                $("#sendCaptcha").prop("disabled", false);  // 启用按钮
                $("#sendCaptcha").text("发送验证码");  // 恢复按钮文本
                countdownTime = 10;  // 重置倒计时
            }
        }, 1000);  // 每隔 1 秒更新一次
    }
});
