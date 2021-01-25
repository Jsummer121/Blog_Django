// @Auther:Summer
$(function () {
    let $img = $(".form-item .captcha-graph-img img"); // 获取图像

    // let $imgCodeText = $('#input_captcha');

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

})