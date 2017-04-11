

// Field Validation
var n = new Notyf({ delay: 5000 });
$(".ask").hide();
$('.submit').on("click", function(e) {
    e.preventDefault();
    flag = 1;
    userName = $("#id_username").val();
    if (userName == "") {
        n.alert("Username is blank.")
        flag = 0;
    }
    if (userName.length < 4 || userName.length > 15) {
        n.alert("Username's character length must be between 4 and 15.")
        flag = 0;
    }
    if ($("#id_email").val() == "") {
        n.alert("Email is blank.")
        flag = 0;
    }
    if ($("#id_password").val() == "") {
        n.alert("Password is blank.")
        flag = 0;
    }
    if ($("#id_confirm_password").val() == "") {
        n.alert("Confirm Password is blank.")
        flag = 0;
    }
    if ($("#id_bio").val() == "") {
        n.alert("Bio is blank.")
        flag = 0;
    }
    if (flag) {
        $(".ask").click();
    }

});
