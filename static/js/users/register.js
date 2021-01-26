// @Auther:Summer
$(function () {
    let $img = $(".form-item .captcha-graph-img img"); // 获取图像
    let $username = $("#user_name");  // get username by id
    let $mobile = $("#mobile"); // get mobile by id
    let $smsCodeBtn = $(".form-item .sms-captcha"); //get sms btn
    let $imageCodeText = $("#input_captcha");  // get image code text
    let $mobileReturnVal = ""; // get mobile return val
    let $usernameRetuenVal = "";  // get username return val
    let $register = $(".form-contain"); // get register form



    generate()  // auto create the first img
    $img.click(generate);  // run generate when img clicked

    // blur,触发失去焦点事件
    $username.blur(function () {
        $usernameRetuenVal = fn_check_username();
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
        let sReturnValue = "";

        // check data null
        if ($sUsername === ""){
            message.showError("用户名不能为空")
            return sReturnValue;
        }
        // use re to check username
        if (!(/^\w{5,20}$/).test($sUsername)){
            message.showError("请输入5-20为字符的用户名")
            return sReturnValue;
        }

        // send ajax report
        $.ajax({
            url: '/username/' + $sUsername + "/",
            async: false, // set ansync(同步)
            type: "GET",
            dataType: "json",
        }).done(function (res){// 成功返回的情况下
            if(res.data.count !== 0){
                message.showError("用户名:" + res.data.username + "已注册，请重新输入")
            }else {
                message.showSuccess("用户名" + res.data.username + "可以正常使用")
                sReturnValue = "success";
            }
        }).fail(
            function () {
                message.showError("服务器超时，请重试！")
            }
        );
        return sReturnValue;
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
                // 设置按钮不可点击
                $smsCodeBtn.attr('disabled',true);
                let num = 60;
                // 设置一个计时器
                let t = setInterval(function () {
                    if (num === 1) {
                        // 如果计时器到最后, 清除计时器对象
                        clearInterval(t);
                        $smsCodeBtn.attr('disabled',false);
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

    // register
    $register.submit(function (e) {
        // prevent default submit
        e.preventDefault();

        // get the value of user input
        let sUsername = $username.val();
        let sPassword = $("input[name=password]").val();
        let sPasswordRepeat = $("input[name=password_repeat]").val();
        let sMobile = $mobile.val();
        let sSmsCode = $("input[name=sms_captcha]").val();

        // check moble
        if ($mobileReturnVal !== "success"){
            return;
        }

        // check username
        if ($usernameRetuenVal !== "success"){
            return;
        }

        // check pass and pass_re whether null
        if ((!sPassword) || (!sPasswordRepeat)){
            message.showError("密码与确认密码不能为空！")
            return;
        }

        // check pass and pass_re len
        if ((sPassword.length < 6 || sPassword.length > 20) ||
            (sPasswordRepeat.length < 6 || sPasswordRepeat.length > 20)) {
            message.showError('密码和确认密码的长度需在6～20位以内！');
            return;
        }

        // chcek pass and pass_re whether same
        if (sPassword !== sPasswordRepeat){
            message.showError("密码和确认密码不一致！");
            return;
        }

        // check sms_code len
        if (!(/^\d{6}$/).test(sSmsCode)) {
            message.showError('短信验证码格式不正确，必须为6位数字！');
            return;
        }

        // request
        // set request data
        let SdataParams = {
            "username": sUsername,
            "password": sPassword,
            "password_repeat": sPasswordRepeat,
            "mobile": sMobile,
            "sms_code": sSmsCode
        };
        // send ajax
        $.ajax({
            url: '/user/register/',
            type:"POST",
            data: JSON.stringify(SdataParams),
            // 请求内容的数据类型（前端发给后端的格式）
            contentType: "application/json; charset=utf-8",
            dataType: "json",
        }).done(function (res) {
            if(res.errno === "0"){
                // regitser OK
                message.showSuccess('恭喜你，注册成功！');
                setTimeout(() => {
                // redirect to login page
                window.location.href = '/user/login/';
                }, 1500)
            }else {
                // register error print errormessage
                message.showError(res.errmsg);
            }
        }).fail(function () {
            message.showError("服务器超时，请重试")
        })
    })
})