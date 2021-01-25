// @Auther:Summer
$(function () {
    let $img = $(".form-item .captcha-graph-img img"); // 获取图像
    let $username = $("#user_name");  // get username by id
    let $mobile = $("#mobile"); // get mobile by id



    generate()  // auto create the first img
    $img.click(generate);  // run generate when img clicked

    // blur,触发失去焦点事件
    $username.blur(function () {
        fn_check_username()
    });
    $mobile.blur(function () {
        fn_check_mobile()
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
        let $sMobile = $mobile.val() // get data

        // check mobile whether null
        if ($sMobile === ""){
            message.showError("手机号不能为空");
            return;
        }

        // use re to check mobile
        if (!(/^1[3-9]\d{9}$/).test($sMobile)){
            message.showError("手机号格式错误，请重新输入")
            return;
        }

        // send sjax
        $.ajax({
            url: "/mobiles/" + $sMobile + "/",
            type: "GET",
            dataType: "json"
        }).done(function (res) {
            if(res.data.count !== 0){
                message.showError("手机号已注册，请重新输入")
            }else{
                message.showSuccess("手机号可以正常使用")
            }
        }).fail(function () {
                message.showError("服务器超时，请重试！")
        })
    }


})