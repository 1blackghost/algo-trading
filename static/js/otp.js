$(document).ready(function(){
  w=2;
  i=59;
  document.getElementById("resend").innerHTML="03:00";
  inter=setInterval(function (){
        document.getElementById("resend").innerHTML="0"+w+":"+i;
        i=i-1;
        if(i<10){
          i="0"+i;
        }
        if(i==0){
          i=59;
          if(w>=0){
            w=w-1;
          }
          if(w==-1){
            clearInterval(inter);
            document.getElementById("resend").innerHTML="Re-send";
          }
      }
  },1000);
});
$(document).ready(function() {
        $("#error").hide();
    initializeOTPVerification();

    $('.Verify').click(function() {
      var otp = '';
      $('.otp-input').each(function() {
        otp += $(this).val();
      });

      submitOTP(otp);
    });
  });

  function initializeOTPVerification() {
      $(document).on('keyup', '.otp-input', function(e) {
          var key = e.keyCode || e.which;
          if (key === 8) {
              var prevId = parseInt($(this).attr('id')) - 1;
              if (prevId >= 1) {
                  $('#' + prevId).focus();
              }
          } else {
              var nextId = parseInt($(this).attr('id')) + 1;
              if (nextId <= 6) {
                  $('#' + nextId).focus();
              }
          }
      });
  }
  function submitOTP(otp) {
    $.ajax({
      url: "/otp",
      method: "POST",
      data: { otp: otp },
      success: function(response) {

          console.log('Success:', response);
          if (response=="ok"){
            window.location.href="/reset_password";
          }
          else if (response == "redirect") {
            window.location.href = "/login?msg=True";
          }

          else{
           window.location.href = '/dashboard';
          }
      },
      error: function(xhr, textStatus, errorThrown) {
          var errorMessage = xhr.responseText;
          console.log(errorMessage);
          $("#error").show();

          $("#error").text(errorMessage);
      }
    });
  }