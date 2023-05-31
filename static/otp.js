$(document).ready(function() {
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
          $("#error").text(response).css("color", "green");

          console.log('Success:', response);
          if (response=="ok"){
            window.location.href="/reset_password";
          }
          else{
           window.location.href = '/dashboard';
          }
      },
      error: function(xhr, textStatus, errorThrown) {
          var errorMessage = xhr.responseText;
          console.log(errorMessage);
          $("#error").text(errorMessage);
      }
    });
  }