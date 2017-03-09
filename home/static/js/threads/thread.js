        //Answer voting
        if(anonFlag == 1){
            alert("Heree");
            (function(){
                'use strict';
                var data = {
                    message: 'Please loggg in to vote'
                };
                $(".snackbar_show").on("click", function(){
                    $("#snackbar_reveals")[0].MaterialSnackbar.showSnackbar(data);
                });
             }());
        }
        else{
            alert("hereoo")
            var simplemde = new SimpleMDE({
                element: $("#MyID")[0],
                hideIcons: ["quote", "fullscreen", "side-by-side"],
                spellChecker: false,
                placeholder: "Type here...",
                renderingConfig: {
                    singleLineBreaks: false,
                    codeSyntaxHighlighting: true,
                },
            });
            alert("Not over there");
            $(".upvote").click(function(){
                vote_url = $(this).data("url");
                id = $(this).data("id");
                $.get(vote_url, function(data, status){
                    $("#up"+id).toggleClass("vote-default").toggleClass("vote-success");
                    $("#down"+id).removeClass("vote-danger").addClass("vote-default")
                    $("#score"+id).children()[0].textContent = data.points;
                });
            });
            $(".downvote").click(function(){
                vote_url = $(this).data("url");
                id = $(this).data("id");
               $.get(vote_url, function(data, status){
                    $("#down"+id).toggleClass("vote-default").toggleClass("vote-danger");
                    $("#up"+id).removeClass("vote-success").addClass("vote-default");
                    $("#score"+id).children()[0].textContent = data.points;
               });
            });
            $(".ansUpvote").click(function() {
                vote_url = $(this).data("url");
                id = $(this).data("id");
                $.get(vote_url, function(data, status) {
                    $("#ansUp" + id).toggleClass("vote-default").toggleClass("vote-success");
                    $("#ansDown" + id).removeClass("vote-danger").addClass("vote-default")
                    $("#ansScore" + id).children()[0].textContent = data.points;
                });
            });
            $(".ansDownvote").click(function() {
                vote_url = $(this).data("url");
                id = $(this).data("id");
                $.get(vote_url, function(data, status) {
                    $("#ansDown" + id).toggleClass("vote-default").toggleClass("vote-danger");
                    $("#ansUp" + id).removeClass("vote-success").addClass("vote-default");
                    $("#ansScore" + id).children()[0].textContent = data.points;
                });
            });
        }

        //Clipboard
        var delayMillis = 1500;
        $(".clipboard_button").click(function() {
            ans_id = $(this).data("id");
            span_id = "#aspan" + ans_id;
            $(span_id).html($(".mdl-tooltip span").html() == 'Permalink' ? 'Copied!' : 'Permalink');
            setTimeout(function() {
                $(span_id).parent().hide()
            }, delayMillis);
            setTimeout(function() {
                $(span_id).html($(".mdl-tooltip span").html() == 'Copied!' ? 'Permalink' : 'Permalink');
                $(span_id).parent().show()
            }, 4000)
        });
        var clipboard = new Clipboard('.clipboard_button');
        
        //Highligting 
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

        // Error Notifications
        var not = new Notyf({
            delay: 5000
        })
        $(".submit").hide();
        $('#submitdummy').on("click", function(e) {
            e.preventDefault();
            flag = 1;
            if (simplemde.value() == "") {
                alert("Write the answer before clicking submit.");
                not.alert("Please write the answer.")
                flag = 0;
            }
            if (flag) {
                $(".submit").click();
            }
        });