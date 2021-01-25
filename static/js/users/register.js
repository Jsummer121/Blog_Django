// @Auther:Summer
$(function () {
    let $img = $(".form-item .captcha-graph-img img"); // 获取图像

    // let $imgCodeText = $('#input_captcha');
    let $username = $("#user_name");  // get username by id

    generate()
    $img.click(generate);
    function generate() {
        sImageCodeId = generateUUID();
        let imageCodeUrl = '/image_code/' + sImageCodeId + '/';
        // let imageCodeUrl = '/demo/';
        $img.attr("src", imageCodeUrl);
    }

    // 生成图片UUID验证码
    function generateUUID() {
    let d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    let uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        let r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
    }

    // blur,触发失去焦点事件
    $username.blur(function () {
        fn_check_username()
    })

    // check the username weather register
    function fn_check_username() {
        // get data
        let $sUsername = $username.val();

        // check data null
        if ($sUsername === ""){
            message.showError("用户名不能为空")
            return;
        }
        // use re to check username
        if (!(/^\w{5,20}$/).test($sUsername)){
            message.showError("请输入5-20为字符的用户名")
            return;
        }

        // send ajax report
        $.ajax({
            url: '/username/' + $sUsername + "/",

            type: "GET",
            dataType: "json",

        }).done(function (res){// 成功返回的情况下
            if(res.data.count !== 0){
                message.showError("用户名:" + res.data.username + "已注册，请重新输入")
            }else {
                message.showSuccess("用户名" + res.data.username + "可以正常使用")
            }
        }).fail(
            function () {
                message.showError("服务器超时，请重试！")
            }
        )
    }
})