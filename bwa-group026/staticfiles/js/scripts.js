
function getCookie(name) {
var cookieValue = null;
if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
console.log(csrftoken);

//Ajax call
function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function accept_friend($this, to)
{
  var url = "/users/"+to+"/"
  $.ajax({
    type: "POST",
    url: url,
    data: {'from_accept': $this.id},
    success : function(f) {
      console.log(f)
      if (f == 'Unauthorized') {
        window.alert("Unauthorized!")
      } else {
        window.alert("Friend added")
        location.reload()
      }
     console.log("requested access complete");
  }
}
  )
}

function decline_friend($this, to)
{
  var url = "/users/"+to+"/"
  $.ajax({
    type: "POST",
    url: url,
    data: {'from_decline': $this.id},
    success : function(f) {
      console.log(f)
      if (f == 'Unauthorized') {
        window.alert("Unauthorized!")
      } else {
        window.alert("Friend request removed")
        location.reload()
        console.log("requested access complete");
      }
  }
}
  )
}

function remove_friend($this, to)
{
  var url = "/users/"+to+"/"
  $.ajax({
    type: "POST",
    url: url,
    data: {'from_remove': $this.id},
    success : function(f) {
      console.log(f)
      if (f == 'Unauthorized') {
        window.alert("Unauthorized!")
      } else {
        window.alert("Friend removed")
        location.reload()
        console.log("requested access complete");
     }
  }
}
  )
}

$('#chat-form').on('submit', function(event){
    event.preventDefault();

    $.ajax({
        url : 'post/',
        type : 'POST',
        data : { 'chat-msg' : $('#chat-msg').val() },

        success : function(json){
            $('#chat-msg').val('');
            $('#msg-list').append('<li class="text-right list-group-item">' + json.msg + '</li>');
            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
        }
    });
});

function getMessages(){
    if (!scrolling) {
        $.get('/messages/', function(messages){
            $('#msg-list').html(messages);
        });
    }
    scrolling = false;
}

var scrolling = false;
$(function(){
    $('#msg-list-div').on('scroll', function(){
        scrolling = true;
    });
    refreshTimer = setInterval(getMessages, 500);
});
