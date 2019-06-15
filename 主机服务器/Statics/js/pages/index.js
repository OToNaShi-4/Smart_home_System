function get_stat() {
    let request = new XMLHttpRequest();
    let url = "/api/get_stat";
    request.open("post", url, true);
    request.setRequestHeader('content-type', 'application/json');
    request.setRequestHeader('X-XSRFToken', getCookie("_xsrf"));
    request.onreadystatechange = function () {
        if (this.readyState == 4) {
            let data = JSON.parse(this.responseText);
            let cb = document.getElementById('btn_cb-1');
            cb.checked = data.stat == '1';
        }
    };
    request.send(JSON.stringify({}))
};

function change_stat() {
    let request = new XMLHttpRequest();
    let url = "/api/change_stat";
    request.open("post", url, true);
    let cb = document.getElementById('btn_cb-1');
    if (cb.checked){
        var stat = 'on'
    }else{
        var stat = 'off'
    }
    var data = {"stat": stat};
    request.setRequestHeader('content-type', 'application/json');
    request.setRequestHeader('X-XSRFToken', getCookie("_xsrf"));
    request.onreadystatechange = function () {
        if (this.readyState == 4) {
            let data = JSON.parse(this.responseText);
            cb.checked = data.stat == '1';
        }
    };
    request.send(JSON.stringify(data))
}