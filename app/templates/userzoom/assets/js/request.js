function get_user_info(){
    var userInfo;
    $.ajax({  
        type: "GET",  
        url:"http://127.0.0.1:8058/user/getinfo",  
        data:{},  
        dataType: 'json',
        contentType: "application/json",
        async: false,  
        error: function(request) {  
            alert("Connection error");  
        },  
        success: function(data) {  
            alert("成功了，小伙子")
            userInfo = data['data'];
        }
    })
    return userInfo;
}

function get_user_main(userSeqid, userInfo){
    var userInfo = get_user_info();
    var artInfo;
    var item1 = '<h2 id="h2num" class="episode__number">';
    var item2 = '</h2><div class="episode__media"><a href="detail.html" class="episode__image"></a></div><div class="episode__detail"><a href="detail.html" id="arttime" class="episode__title"><h4>';
    var item3 = '</h4></a><p id="arttext" class="episode__description">';
    var item4 = 'arttext</p></div>';

    $.ajax({  
        type: "GET",  
        url:"http://127.0.0.1:8058/article/get",  
        data:{artUserid:userSeqid},  
        dataType: 'json',
        contentType: "application/json",
        async: false,  
        error: function() {  
            alert("Connection error");  
        },  
        success: function(data) {  
            alert("成功了，小伙子")
            artInfo = data['data'];
        }
    })
    // 渲染用户信息
    if (userInfo['nickname']){
        document.getElementById("username").innerHtml = userInfo['nickname']
    }else{
        document.getElementById("username").innerHtml = userInfo['phoneNumber']
    }
    document.getElementById("interview").innerHTML = userInfo['interview']
    // 渲染动态信息
    var len = Object.keys(artInfo).length;
    if (len > 0){
        var fatherTag = document.getElementById("fatherSection");
        for(var i=0; i<len; i++){
            let newTag = document.createElement("article");
            newTag.setAttribute("class", "episode");
            let html = item1 + '0' + i + item2 + artInfo['doTime'] + item3 + artInfo['text'] + item4;
            newTag.innerHTML = html;
            fatherTag.appendChild(newTag)
            if (i=4){
                break;
            }
        }
    }


}