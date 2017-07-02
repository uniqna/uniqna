(function(){

    // Pagination for All, Questions and Answers
    var all_page = 0;
    $('#all-panel').jscroll({
        loadingHtml: '<center><div class="mdl-spinner mdl-js-spinner is-active loader"></div></center><script>componentHandler.upgradeElement($(".loader")[0])<\/script>',
        autoTrigger: false,
        nextSelector: '.endless_page_link',
        contentSelector: '.all_content',
        callback: function() {
            $("#all-panel .pagination")[all_page].hidden = true;
            all_page += 1;
        }
    });
    var questions_page = 0;
    $('#questions-panel').jscroll({
        loadingHtml: '<center><div class="mdl-spinner mdl-js-spinner is-active loader"></div></center><script>componentHandler.upgradeElement($(".loader")[0])<\/script>',
        autoTrigger: false,
        nextSelector: '.endless_page_link',
        contentSelector: '.questions_content',
        callback: function() {
            $("#questions-panel .pagination")[questions_page].hidden = true;
            questions_page += 1;
        }
    });
    var answers_page = 0;
    $('#answers-panel').jscroll({
        loadingHtml: '<center><div class="mdl-spinner mdl-js-spinner is-active loader"></div></center><script>componentHandler.upgradeElement($(".loader")[0])<\/script>',
        autoTrigger: false,
        nextSelector: '.endless_page_link',
        contentSelector: '.answers_content',
        callback: function() {
            $("#answers-panel .pagination")[answers_page].hidden = true;
            answers_page += 1;
        }
    });
    // Voting scripts
    if (anonFlag == 1) {
        (function() {
            'use strict';
            var data = {
                message: 'Please log in to vote'
            };
            $(".snackbar_show").on("click", function() {
                $("#snackbar_reveals")[0].MaterialSnackbar.showSnackbar(data);
            });
        }());
    } else {
        $(".tab-container").on("click", ".upvote", function() {
            vote_url = $(this).data("url");
            id = $(this).data("id");
            $.get(vote_url, function(data, status) {
                $(".up" + id).toggleClass("vote-default").toggleClass("vote-success");
                $(".down" + id).removeClass("vote-danger").addClass("vote-default")
                $(".score" + id).children()[0].textContent = data.points;
            });
        });
        $(".tab-container").on("click", ".downvote", function() {
            vote_url = $(this).data("url");
            id = $(this).data("id");
            $.get(vote_url, function(data, status) {
                $(".down" + id).toggleClass("vote-default").toggleClass("vote-danger");
                $(".up" + id).removeClass("vote-success").addClass("vote-default");
                $(".score" + id).children()[0].textContent = data.points;
            });
        });
        $(".tab-container").on("click", ".ansUpvote", function() {
            vote_url = $(this).data("url");
            id = $(this).data("id");
            $.get(vote_url, function(data, status) {
                $(".ansUp" + id).toggleClass("vote-default").toggleClass("vote-success");
                $(".ansDown" + id).removeClass("vote-danger").addClass("vote-default")
                $(".ansScore" + id).children()[0].textContent = data.points;
            });
        });
        $(".tab-container").on("click", ".ansDownvote", function() {
            vote_url = $(this).data("url");
            id = $(this).data("id");
            $.get(vote_url, function(data, status) {
                $(".ansDown" + id).toggleClass("vote-default").toggleClass("vote-danger");
                $(".ansUp" + id).removeClass("vote-success").addClass("vote-default");
                $(".ansScore" + id).children()[0].textContent = data.points;
            });
        });
    }
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

    // Toggle email notification
    $("#email_notification").on("change", function(){
        var data = {
            toggle: $(this).is(":checked")
        };
        var purl = $("#toggle_url").val();
        $.post(purl, data).fail(function(data){
            console.error("Email toggle failed.");
        });
    });

    //Code Highlighting
    hljs.initHighlightingOnLoad();

    //Google Analytics
    (function(i, s, o, g, r, a, m) {
        i['GoogleAnalyticsObject'] = r;
        i[r] = i[r] || function() {
            (i[r].q = i[r].q || []).push(arguments)
        }, i[r].l = 1 * new Date();
        a = s.createElement(o),
            m = s.getElementsByTagName(o)[0];
        a.async = 1;
        a.src = g;
        m.parentNode.insertBefore(a, m)
    })(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');

    ga('create', 'UA-91622346-1', 'auto');
    ga('send', 'pageview');

})();
