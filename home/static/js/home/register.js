//Constants 

const school_select = "#id_school";

const chennai_school_choices = {
    "SCSE": "SCSE",
    "SENSE": "SENSE",
    "SAS": "SAS",
    "SELECT": "SELECT",
    "SMBS": "SMBS",
    "VITBS": "VITBS",
    "VITSOL": "VITSOL",
    "VFIT": "VFIT",
}
const vellore_school_choices = {
    "SAS": "SAS",
    "V-SPARC": "V-SPARC",
    "SBST": "SBST",
    "SCALE": "SCALE",
    "SCOPE": "SCOPE",
    "SITE": "SITE",
    "SMEC": "SMEC",
    "SSL": "SSL",
    "SELECT": "SELECT",
    "VITBS": "VITBS",
    "VITSOL": "VITSOL",
    "VFIT": "VFIT"
}

function update_select(selector, options) {
    // Removes all the options first
    // Then appends the new ones from the options
    var schools = $(selector);
    schools.empty();
    $.each(options, function(key, value) {
        schools.append($("<option></option>").attr("value", value).text(key));
    });
}

// Initially populating select with Chennai Choices
update_select(school_select, chennai_school_choices);

// Event handler functions for dynamic update
$("#id_university").on("change", function(e) {
    if (this.value == "Vellore Institute of Technology, Vellore") {
        update_select(school_select, vellore_school_choices);
    } else if (this.value == "Vellore Institute of Technology, Chennai") {
        update_select(school_select, chennai_school_choices);
    }
});

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
