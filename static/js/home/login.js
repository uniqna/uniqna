
(function() {

    // Field validation
    var n = new Notyf({ delay: 5000 });
    $(".login").hide();
    $('.submit').on("click", function(e) {
        e.preventDefault();
        flag = 1;
        if ($("#username").val() == "") {
            n.alert("Username is blank.")
            flag = 0;
        }
        if ($("#password").val() == "") {
            n.alert("Password is blank.")
            flag = 0;
        }
        if (flag) {
            $(".login").click();
        }
    });

    //Shifting field focus
    $("#username").on("keypress", function(e){
        // Whenever enter is pressed this shifts the focus to 
        // password input instead of submitting
        if (e.which == 13){
            e.preventDefault();
            e.stopPropagation();
            $("#password").focus();
        }
    });

    // Focus on username field when logged in 
    $("#username").focus();

})();
