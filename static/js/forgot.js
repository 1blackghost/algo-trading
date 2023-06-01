$(document).ready(function() {
    $('#loginForm').submit(function(e) {
      e.preventDefault();
      $("#error").hide();
      
      var email = $('#email').val();
      
      get_otp(email);
    });
  });
  
  function get_otp(email) {
    $.ajax({
      url: "/forgot_password",
      method: "POST",
      data: { email: email },
      success: function(response) {
        $("#error").text(response).css("color", "green");

        console.log('Success:', response);
        window.location.href = '/otp';
        },
      error: function(xhr, textStatus, errorThrown) {
        var errorMessage = xhr.responseText;
        console.log(errorMessage);
        $("#error").show();

        $("#error").text(errorMessage);
        }
    });
  }
  function load(){
    var load=document.getElementById("lo");
    if(document.getElementById("email").value){
    load.innerHTML='';
    load.innerHTML='<img class="load">';
    }
    else{
      load.innerHTML='Get OTP';
    }
  }
