// チャットボットのメッセージを画面に表示する関数
var chatassistant = function(chat, model) {
    var chattxt = '<div class="sb-side sb-side-left"><div class="assistant">' + chat + '</div>' + 'モデル：' + model + '</div>';
    $('#chat').append(chattxt);
}

// ユーザーのメッセージを画面に表示する関数
var chatuser = function(chat) {
    var chattxt = '<div class="sb-side sb-side-right"><div class="user">' + chat + '</div></div>';
    $('#chat').append(chattxt);
}

// モデル切り替え時の処理
$(function() {
    $('.tab').on('click', function() {
        $('.tab').removeClass('active');
        $(this).addClass('active');
    });
});

// メッセージを送信する関数
function post() {
    var button = $("#button");
    button.attr("disabled", true);

    var text = $("#text").val();
    console.log(text);

    var lists = Array.from(document.querySelectorAll("li"));
    var index = lists.findIndex(list => Array.from(list.classList).includes("active"));
    var model = "";
    
    if (index === 0) {
        model = "llama2";
    } else if (index === 1) {
        model = "line_llm";
    } else if (index === 2) {
        model = "東大_llm";
    }
    console.log(model);

    var data = {"question": text, "model": model};
    var posturl = "http://localhost:8000/process/";

    chatuser(text);

    var container = document.getElementById('chat');
    if (!isScrollBottom(container)) {
        scrollToBottom(container);
    }

    $.ajax({
        type: "post",
        timeout: 4000000,
        url: posturl,
        strictSSL: false,
        dataType: "json",
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function(jsondata) {
            if (jsondata.code == "9") {
                chatassistant("エラー（応答が遅いなど）");
            } else {
                chatassistant(jsondata.answer, model);
                console.log(jsondata.answer);
            }
            
            container = document.getElementById('chat');
            if (!isScrollBottom(container)) {
                scrollToBottom(container);
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            console.log("error");
            chatassistant(textStatus);
            
            container = document.getElementById('chat');
            if (!isScrollBottom(container)) {
                scrollToBottom(container);
            }
        },
        complete: function() {
            button.attr("disabled", false);
            $("#text").val("");
            
            container = document.getElementById('chat');
            if (!isScrollBottom(container)) {
                scrollToBottom(container);
            }
        }
    });
}

// 自動スクロール処理
var scrollToBottom = (target) => {
    target.scrollTop = target.scrollHeight;
};

var isScrollBottom = (target) => {
    return target.scrollHeight === target.scrollTop + target.offsetHeight;
};

// ボタンが押されたときに実行されるもの
$(function(){
    $("#button").click(function(event){
        post();
    });
});

// Enterキーが押されたときに実行されるもの
function handleEnterKey(event) {
    if (event.keyCode === 13) {
        if ($('#button').attr("disabled") == false) {
            post();
        }
    }
}
const inputElement = document.getElementById("text");
inputElement.addEventListener("keydown", handleEnterKey);

// ログインボタンが押されたときに実行されるもの
document.getElementById("login").addEventListener("click", function () {
    location.replace('http://localhost:8000/');
}, false);
