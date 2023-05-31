$(document).ready(function() {
    $('#signup-form').submit(function(event) {
        event.preventDefault(); 
        signUp();
    });
});

function signUp() {
    var password = $('#password').val();
    var confirmPassword = $('#confirm-password').val();

    $.ajax({
        url: '/reset_password',
        method: 'POST',
        data: {
            password: password,
            confirmPassword: confirmPassword
        },
        success: function(response) {
            $("#error").text(response).css("color", "green");
            
            console.log('Success:', response);
            setTimeout(function() {
            console.log("Next line of code");
            }, 1000);            
            window.location.href = '/dashboard';
        },
        error: function(xhr, textStatus, errorThrown) {
            var errorMessage = xhr.responseText;
            console.log(errorMessage);
            $("#error").text(errorMessage);
            $("html, body").animate({ scrollTop: 0 }, "slow");


            
        }
    });
}