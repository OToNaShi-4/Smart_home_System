function register() {
    let user_email = document.getElementById('user_email').value;
    let user_name = document.getElementById('user_name').value;
    let user_pwd = document.getElementById('user_pwd').value;
    let user_pwd2 = document.getElementById('user_pwd2').value;
    if (user_pwd == user_pwd2){
        let request = new XMLHttpRequest();
        let url = "/register";
        request.open("post", url, true);
        var data = {"user_email": user_email, "user_pwd": user_pwd,"user_name": user_name};
        request.setRequestHeader('content-type', 'application/json');
        request.setRequestHeader('X-XSRFToken', getCookie("_xsrf"));
        request.onreadystatechange = function () {
            if (this.readyState == 4) {
                let data = JSON.parse(this.responseText);
                if (data.err_code == '200') {
                    window.location.href = '/login'
                }else if (data.err_code == '420'){
                    alert(data.err_msg)
                }
            }
        };
        request.send(JSON.stringify(data))
    }
    else {
        alert('两次密码不匹配')
    }
}
