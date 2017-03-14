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
        $(".upvote").on("click", function() {
            vote_url = $(this).data("url");
            id = $(this).data("id");
            $.get(vote_url, function(data, status) {
                $("#up" + id).toggleClass("vote-default").toggleClass("vote-success");
                $("#down" + id).removeClass("vote-danger").addClass("vote-default")
                $("#score" + id).children()[0].textContent = data.points;
            });
        });
        $(".downvote").on("click", function() {
            vote_url = $(this).data("url");
            id = $(this).data("id");
            $.get(vote_url, function(data, status) {
                $("#down" + id).toggleClass("vote-default").toggleClass("vote-danger");
                $("#up" + id).removeClass("vote-success").addClass("vote-default");
                $("#score" + id).children()[0].textContent = data.points;
            });
        });
        $(".ansUpvote").on("click", function() {
            vote_url = $(this).data("url");
            id = $(this).data("id");
            $.get(vote_url, function(data, status) {
                $(".ansUp" + id).toggleClass("vote-default").toggleClass("vote-success");
                $(".ansDown" + id).removeClass("vote-danger").addClass("vote-default")
                $(".ansScore" + id).children()[0].textContent = data.points;
            });
        });
        $(".ansDownvote").on("click", function() {
            vote_url = $(this).data("url");
            id = $(this).data("id");
            $.get(vote_url, function(data, status) {
                $(".ansDown" + id).toggleClass("vote-default").toggleClass("vote-danger");
                $(".ansUp" + id).removeClass("vote-success").addClass("vote-default");
                $(".ansScore" + id).children()[0].textContent = data.points;
            });
        });
    }

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
