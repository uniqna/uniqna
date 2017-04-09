 //Initializing simplemde object
 var simplemde;

 //Default progress bar
 document.querySelector('#p3').addEventListener('mdl-componentupgraded', function() {
     this.MaterialProgress.setProgress(0);
     this.MaterialProgress.setBuffer(0);
 });

 $(document).ready(function() {
     simplemde = new SimpleMDE({
         element: $("[name=description]")[1],
         hideIcons: ["quote", "fullscreen"],
         spellChecker: false,
         placeholder: "A follow up description...",
     });
 });

 //Add new tag
 $("#newtagdiv").hide();
 $(".tagcreated").hide();
 $(".blank-error").hide();
 $("#addtag").click(function() {
     $("#newtagdiv").show();
 });

 //Getting csrf token from stored cookie
 function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie !== '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = jQuery.trim(cookies[i]);
             if (cookie.substring(0, name.length + 1) === (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 }
 var csrftoken = getCookie('csrftoken');
 //Attachign the token to the rest header
 function csrfSafeMethod(method) {
     // these HTTP methods do not require CSRF protection
     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
 }
 $.ajaxSetup({
     beforeSend: function(xhr, settings) {
         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
             xhr.setRequestHeader("X-CSRFToken", csrftoken);
         }
     }
 });

 //Update Progress
 $(document).ready(function() {
     $(".CodeMirror-scroll").blur(function() {
         if (simplemde.value()) {
             $("#p3")[0].MaterialProgress.setBuffer(100)
         }
     })
 });

 //Replace spaces while creating tags with underscore
 $("#newtag").on("keyup", function(e) {
     vals = this.value;
     modified = vals.replace(/ /g, '_');
     if (vals != modified) {
         this.value = modified;
     }
 });

 //Create Tag
 var fail;
 $("#create_tag").click(function() {
    var purl = $(this).data("url");
    console.log(purl);
     var data = {
         "name": $("#newtag").val()
     }
     $.post(purl, data, function(data, status) {
         document.getElementById("newtag").value = ""
         $(".tagcreated").fadeIn(2000).fadeOut(2000);
         $("#newtagdiv").hide()
         document.getElementById("tags_input").value = document.getElementById("tags_input").value + "," + data.name
         $(".flexdatalist-multiple").prepend("<li class='value'><span class='text'>" + data.name + "</span><span class='fdl-remove custom-remove' data-name='" + data.name + "'>×</span></li>");
         $(".custom-remove").off("click");
         $(".custom-remove").on("click", function() {
             var container = $(this).parent();
             var _vals = document.getElementById("tags_input").value.split(",");
             var toRemove = _vals.indexOf($(this).data("name"));
             _vals.splice(toRemove, 1);
             document.getElementById("tags_input").value = _vals.join(",");
             container.remove();
         });
     }).fail(function(data) {
         alert("Tag already exists");
     })
 });

 //Get suggested tags and append to #suggested.
 var surl = $(".suggest-url").data("url");
 $(".mdl-textfield__input").blur(function() {
     if ($(this).val()) {
         $("#p3")[0].MaterialProgress.setBuffer(50);
         $.post(surl, {
             "text": $(this).val()
         }, function(data, status) {
             if (data.length) {
                 vals = document.getElementById("tags_input").value.split(",");

                 function validateData(obj) {
                     for (i = 0; i < vals.length; i++) {
                         if (obj.name == vals[i]) {
                             return 0;
                         }
                     }
                     return 1;
                 }
                 var validated = data.filter(validateData);
                 for (var i = 0; i < (validated.length); i++) {
                     vals.push(validated[i].name);
                     $(".flexdatalist-multiple").prepend("<li class='value'><span class='text'>" + validated[i].name + "</span><span class='fdl-remove custom-remove' data-name='" + validated[i].name + "'>×</span></li>");
                 }
                 document.getElementById("tags_input").value = vals.join(",");
                 $(".custom-remove").off("click");
                 $(".custom-remove").on("click", function() {
                     var container = $(this).parent();
                     var _vals = document.getElementById("tags_input").value.split(",");
                     var toRemove = _vals.indexOf($(this).data("name"));
                     _vals.splice(toRemove, 1);
                     alert(toRemove + " " + _vals);
                     document.getElementById("tags_input").value = _vals.join(",");
                     container.remove();
                 });
             }
         });
     }
 });

 //Client side error
 var n = new Notyf({
     delay: 5000
 });

 //Submit the question
 $(".submit").hide();
 $('#submitdummy').on("click", function(e) {
     e.preventDefault();
     flag = 1;
     if ($("#id_title").val() == "") {
         n.alert("Please enter a Title")
         flag = 0;
     }
     if ($("#id_title").val().length <= 10 && $("#id_title").val().length != "") {
         n.alert("Title is too short")
         flag = 0;
     }
     if (simplemde.value() == "") {
         n.alert("Please enter a Description")
         flag = 0;
     }
     if (flag) {
         $(".submit").click();
     }

 });
