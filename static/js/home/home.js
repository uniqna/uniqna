// Pagination
        var last_page = $("#last").data("last");
        var curr_page = 1;
        $('#infini').jscroll({
            loadingHtml: '<center><div class="mdl-spinner mdl-js-spinner is-active loader"></div></center><script>componentHandler.upgradeElement($(".loader")[0])<\/script>',
            autoTrigger: false,
            nextSelector: '.endless_page_link',
            contentSelector: '.iquestion',
            callback: function() {
                $(".pagination")[curr_page - 1].hidden = true;
                curr_page += 1;
            }
        });
// Voting script
        $(".upvote").click(function() {
            vote_url = $(this).data("url");
            id = $(this).data("id");
            $.get(vote_url, function(data, status) {
                $("#up" + id).toggleClass("vote-default").toggleClass("vote-success");
                $("#down" + id).removeClass("vote-danger").addClass("vote-default")
                $("#score" + id).children()[0].textContent = data.points;
            });
        });
        $(".downvote").click(function() {
            vote_url = $(this).data("url");
            id = $(this).data("id");
            $.get(vote_url, function(data, status) {
                $("#down" + id).toggleClass("vote-default").toggleClass("vote-danger");
                $("#up" + id).removeClass("vote-success").addClass("vote-default");
                $("#score" + id).children()[0].textContent = data.points;
            });
        });
// Floating button script
        var fabState = 1; // Variable denoting the state of the fab
        // 1 - its closed
        // 0 - its open
        $(".hidden-fab").hide();
        // Creating an overlay div which covers the entire screen
        // to prevent the clicking of links
        $(".overlay").css({
            "position": "absolute",
            "width": $(document).width(),
            "z-index": -9,
        });
        $(".create-fab").click("on", function(){
            if (fabState===1){
                $(".wrapper")[0].style.opacity=0.3;
                $(".hidden-fab").show();
                $(".create-fab")[0].style.background = "#eee";
                $(".create-fab")[0].style.color = "#aaa";
                $(".overlay")[0].style.zIndex = 9;
                fabState = 0;
            }
            else if (fabState===0){
                $(".create-fab")[0].style.background = "rgb(255, 204, 77)";
                $(".create-fab")[0].style.color = "#fff";
                $(".hidden-fab").hide()
                $(".wrapper")[0].style.opacity=1;
                $(".overlay")[0].style.zIndex = -9;
                fabState = 1;
            }
        });
        // Link redirection
        $(".hidden-fab").on("click", function(){
            re_url = $(this).data("url");
            document.location = re_url;
        });


// G-Analytics
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
