function scrollin(widt){
    document.getElementById('loginoption').scrollLeft=widt;
  }
  function cancel(inpu){
    document.getElementById('background').style.display=inpu;
  }
  function disp(){
    let popup=document.getElementById("loginsucess");

    if(popup.style.display=="inherit"){
        if(document.getElementById("email").focus){
            popup.style.display="none";
        }
    }

  }
  function detect(x,elemid){
    let opt=document.querySelectorAll(".opt");
    let i=0;

    document.getElementById(elemid).disabled=false;
    if(x==0||x==1){
      for (i=0;i<2;i++){
        opt[i].style.border="3px solid white";
      }
      opt[x].style.border="3px solid red";
    }
    if(x==2||x==3){
      for (i=2;i<4;i++){
        opt[i].style.border="3px solid white";
      }
      opt[x].style.border="3px solid red";
    }
  }
  $(document).ready(function() {
    $('#loginForm').submit(function(e) {
      e.preventDefault();
      
      var email = $('#email').val();
      var password = $('#password').val();
      
      login(email, password);
    });
  });
  
  function login(email, password) {
    $.ajax({
      url: "/login",
      method: "POST",
      data: { email: email, password: password },
      success: function(response) {
        $("#error").text(response).css("color", "green");

        console.log('Success:', response);
        window.location.href = '/dashboard';
        },
      error: function(xhr, textStatus, errorThrown) {
        var errorMessage = xhr.responseText;
        console.log(errorMessage);
        $("#error").text(errorMessage);
        }
    });
  }