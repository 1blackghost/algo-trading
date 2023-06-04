$(document).ready(function() {
  $("#error").hide();
    $('#loginForm').submit(function(e) {
      e.preventDefault();
      
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
        window.var1=errorMessage;
        }
    });
  }
  function load(){
  setTimeout(function load2(){
    var load=document.getElementById("lo");
    var email=document.getElementById("email");
    
    if(email.value){
    load.innerHTML='<img class="load">';
    console.log("load");
    }
    if (var1){
      load.innerHTML='Get OTP';
      console.log("no load");
    } 
  },500);
}
