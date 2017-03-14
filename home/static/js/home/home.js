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
