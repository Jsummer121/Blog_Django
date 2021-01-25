// @Auther:Summer
$(function () {
    let $img = $(".form-item .captcha-graph-img img"); // 获取图像
    let $username = $("#user_name");  // get username by id
    let $mobile = $("#mobile"); // get mobile by id
    let $smsCodeBtn = $(".form-item .sms-captcha"); //get sms btn
    let $imageCodeText = $("#input_captcha");  // get image code text
    let $mobileReturnVal = ""; // get mobile return val



    generate()  // auto create the first img
    $img.click(generate);  // run generate when img clicked

    // blur,触发失去焦点事件
    $username.blur(function () {
        fn_check_username()
    });
    $mobile.blur(function () {
        $mobileReturnVal = fn_check_mobile();
    });

    // the fun to send url to get img
    function generate() {
        sImageCodeId = generateUUID();
        let imageCodeUrl = '/image_code/' + sImageCodeId + '/';
        // let imageCodeUrl = '/demo/';
        $img.attr("src", imageCodeUrl);
    }

    // the fun to create uuid_code
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

    // check the username whether register
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
        );
    }

    // check the mobile whether register
    function fn_check_mobile() {
        let sMobile = $mobile.val(); // get data
        let sReturnValue = "";

        // check mobile whether null
        if (sMobile === ""){
            message.showError("手机号不能为空");
            return sReturnValue
        }

        // use re to check mobile
        if (!(/^1[3-9]\d{9}$/).test(sMobile)){
            message.showError("手机号格式错误，请重新输入")
            return sReturnValue
        }

        // send sjax
        $.ajax({
            url: "/mobiles/" + sMobile + "/",
            type: "GET",
            dataType: "json",
            async: false
        }).done(function (res) {
            if(res.data.count !== 0){
                message.showError("手机号已注册，请重新输入")
            }else{
                message.showSuccess("手机号可以正常使用");
                sReturnValue = "success"
            }
        }).fail(function () {
            message.showError("服务器超时，请重试！")
        });
        return sReturnValue;
    }

    // send sms
    $smsCodeBtn.click(function () {
        // check mobile
        if ($mobileReturnVal !== "success"){
            return;
        }

        // check imgCode
        let text = $imageCodeText.val() // get imagecode
        if (!text){
            message.showError("请输入验证码");
            return;
        }

        // check imgUuid
        if (!sImageCodeId){
            message.showError("图形uuid为空");
            return;
        }

        let dataParams = {
            "mobile": $mobile.val(),
            "text": text,
            "image_code_id":sImageCodeId,
        }
        // send ajax
        $.ajax({
            url: "/sms_code/",
            type: "POST",
            data: JSON.stringify(dataParams),
            dataType: "json"
        }).done(function (res) {
            if (res.errno === "0") {
                // 倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
                message.showSuccess('短信验证码发送成功');
                let num = 60;
                // 设置一个计时器
                let t = setInterval(function () {
                    if (num === 1) {
                        // 如果计时器到最后, 清除计时器对象
                        clearInterval(t);
                        // 将点击获取验证码的按钮展示的文本恢复成原始文本
                        $smsCodeBtn.html("重新发送验证码");
                    } else {
                        num -= 1;
                        // 展示倒计时信息
                        $smsCodeBtn.html(num + "秒");
                    }
                }, 1000);
        } else {
            message.showError(res.errmsg);
        }}).fail(function(){
          message.showError('服务器超时，请重试！');
        });
    })

})