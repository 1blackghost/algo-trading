
$(document).ready(function() {
    $("#error").hide();

    $('#signup-form').submit(function(event) {
        event.preventDefault(); 
        signUp();
    });
});

function signUp() {
    var businessName = $('#business-name').val();
    var email = $('#email').val();
    var mobile = $('#mobile').val();
    var password = $('#password').val();
    var confirmPassword = $('#confirm-password').val();

    $.ajax({
        url: '/signup',
        method: 'POST',
        data: {
            businessName: businessName,
            email: email,
            mobile: mobile,
            password: password,
            confirmPassword: confirmPassword
        },
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
            $("html, body").animate({ scrollTop: 0 }, "slow");


            
        }
    });
}