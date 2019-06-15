function login() {
    let user_email = document.getElementById('user_email').value;
    let user_pwd = document.getElementById('user_pwd').value;
    let request = new XMLHttpRequest();
    let url = "/login";
    request.open("post", url, true);
    var data = {"user_email": user_email, "user_pwd": user_pwd};
    request.setRequestHeader('content-type', 'application/json');
    request.setRequestHeader('X-XSRFToken', getCookie("_xsrf"));
    request.onreadystatechange = function () {
        if (this.readyState == 4) {
            let data = JSON.parse(this.responseText);
            if (data.err_code == '200') {
                window.location.href = '/'
            }
            if (data.err_code == '400'){
                alert(data.err_msg)
            }
            //console.log(this.responseText)
        }
    };
    request.send(JSON.stringify(data))
}
