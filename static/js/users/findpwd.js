// @Auther:Summer
$(function () {
    let $img = $(".form-item .captcha-graph-img img"); // get img
    let $mobile = $("#mobile");
    let $smsCodeBtn = $(".form-item .sms-captcha"); //get sms btn
    let $mobileRetuenVal = ""; // this is run mobile_fun return val
    let $changePsw = $(".register-btn")

    generate();
    $img.click(generate);

    $mobile.blur(function () {
        $mobileRetuenVal = fn_check_mobile();
    })

    // set make img fun
    function generate() {
        imageUUID = generateUUID();
        let imageUrl = "/image_code/" + imageUUID +"/";
        $img.attr("src", imageUrl)
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

    // to check mobile whether register
    function fn_check_mobile() {
        let sRetuenVal = "";
        let sMobile = $mobile.val();  // get mobile val

        // check mobile whether null
        if(sMobile === ""){
            message.showError("手机号不能为空");
            return sRetuenVal;
        }

        // use re to check mobile
        if (!(/^1[3-9]\d{9}$/).test(sMobile)){
            message.showError("手机号格式错误，请重新输入");
            return sRetuenVal;
        }

        // send ajax
        $.ajax({
            url: "/mobiles/" + sMobile + "/",
            type: "GET",
            dataType: "json",
            async: false
        }).done(function (res) {
            if(res.data.count !== 1){
                message.showError("输入的手机号有误，请重新输入");
            }else{
                message.showSuccess("手机号输入正确");
                sRetuenVal = "success";
            }
        }).fail(function () {
            message.showError("服务器超时，请重试");
        })
        return sRetuenVal;
    }

    // send sms
    $smsCodeBtn.click(function () {
        // check moile
        if($mobileRetuenVal !== "success"){
            message.showError("请输入正确的手机号");
            return;
        }

        // get val
        let text = $("#input_captcha").val();

        // check code
        if(!text){
            message.showError("请输入验证码");
            return;
        }

        // check uuid of img
        if(!imageUUID){
            message.showError("图片uuid码为空");
            return;
        }

        // set data
        let sDataParm = {
            "mobile": $mobile.val(),
            "text": text,
            "image_code_id": imageUUID
        }

        // send ajax
        $.ajax({
            url: "/sms_code/",
            type: "POST",
            data: JSON.stringify(sDataParm),
            dataType: "json"
        }).done(function (res) {
            if(res.errno === "0"){
                message.showSuccess("短信验证码发送成功")
                $smsCodeBtn.attr('disabled',true);
                let num = 60;
                let t = setInterval(function () {
                    if(num === 1){
                        // 如果计时器到最后, 清除计时器对象
                        clearInterval(t);
                        $smsCodeBtn.attr('disabled',false);
                        // 将点击获取验证码的按钮展示的文本恢复成原始文本
                        $smsCodeBtn.html("重新发送验证码");
                    }else {
                        num -= 1;
                        $smsCodeBtn.html(num + "秒");
                    }
                },1000
            )}else{
                message.showError(res.errmsg);
        }}).fail(
            message.showError("服务器超时，请重试")
        )
    })

    // change psw
    $changePsw.submit(function (e) {
        // prevent default submit
        e.preventDefault();

        // check moile
        if($mobileRetuenVal !== "success"){
            message.showError("请输入正确的手机号");
            return;
        }

        // get all val
        let sPassword = $("input[name=password]").val();
        let sPasswordRepeat = $("input[name=password_repeat]").val();
        let sMobile = $mobile.val();
        let sSmsCode = $("input[name=sms_captcha]").val();

        // check password
        if((!sPassword) || (!sPasswordRepeat)){
            message.showError("密码与确认密码不能为空")
            return;
        }

        // check passwd len
        if((sPassword.length < 6 || sPassword.length > 20) ||
            (sPasswordRepeat.length < 6 || sPasswordRepeat.length > 20)){
            message.showError("密码和确认密码的长度需在6-20位")
            return;
        }

        // check pass and pass_re whether same
        if(sPassword !== sPasswordRepeat){
            message.showError("密码和确认密码不一致")
            return;
        }

        // check smscode len
        if(!(/^\d{6}$/).test(sSmsCode)){
            message.showError("短信验证码格式不正确，必须是6位数字！")
            return;
        }

        // request
        // set request data
        let SdataParams = {
            "password": sPassword,
            "password_repeat": sPasswordRepeat,
            "mobile": sMobile,
            "sms_code": sSmsCode
        };

        console.log("111")
        console.log(SdataParams)
        // send ajax
        $.ajax({
            url: "/user/findpwd/",
            type:"POST",
            data: JSON.stringify(SdataParams),
            // 请求内容的数据类型（前端发给后端的格式）
            contentType: "application/json; charset=utf-8",
            dataType: "json",
        }).done(function (res) {
            if(res.errno === "0"){
                message.showSuccess("修改密码成功");
                setTimeout(() =>{
                    // redirect to login page
                    window.location.href = '/user/login/';
                },1500)
            }else{
                message.showError(res.errmsg);
            }
        }).fail(function () {
            message.showError("服务器超时，请重试")
        })
    })






});