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
