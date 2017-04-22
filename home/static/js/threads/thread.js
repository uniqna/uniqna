        //Answer voting
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
          var simplemde = new SimpleMDE({
            element: $("#MyID")[0],
            hideIcons: ["quote", "fullscreen", "side-by-side"],
            spellChecker: false,
            placeholder: "This is where you type...",
            forceSync: true,
            renderingConfig: {
              singleLineBreaks: false,
              codeSyntaxHighlighting: true,
            },
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
          $(".ansUpvote").click(function() {
                vote_url = $(this).data("url");
                id = $(this).data("id");
                $.get(vote_url, function(data, status) {
                    $(".ansUp" + id).toggleClass("vote-default").toggleClass("vote-success");
                    $(".ansDown" + id).removeClass("vote-danger").addClass("vote-default")
                    $(".ansScore" + id).children()[0].textContent = data.points;
                });
            });
            $(".ansDownvote").click(function() {
                vote_url = $(this).data("url");
                id = $(this).data("id");
                $.get(vote_url, function(data, status) {
                    $(".ansDown" + id).toggleClass("vote-default").toggleClass("vote-danger");
                    $(".ansUp" + id).removeClass("vote-success").addClass("vote-default");
                    $(".ansScore" + id).children()[0].textContent = data.points;
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
            alert("C'mon! Your thoughts can't be this empty...");
            // not.alert("Please write the answer.")
            flag = 0;
          }
          if (flag) {
            $(".submit").click();
          }
        });

        var leafs = $(".leaf-node");
        var threshold = 3;
        $.each(leafs, function(index, leaf) {
          var parentNodes = $(leaf).parents(".child");
          var level = parentNodes.length + 1;
          var readThreadElement = "<a class='readthread'>Read the full train [ " + (level - threshold) + ((level - threshold) > 1 ? " Replies" : " Reply") + " ]</a>";
          if (level > threshold) {
            // parentNodes[level-threshold-1] will always be a 3rd level node
            // we want to remove every node after that level
            for (var i = level - threshold - 1; i >= 0; i--) {
              parentNodes[i].style.display = "none";
            }
            // Element to attach the "Read Thread" link
            var container = $(parentNodes[level - threshold - 1]).closest(".reply_parent");
            //Check whether a "read Thread" link is already present
            if (container.children(".readthread").length == 0) {
              container.append($(readThreadElement));
            }
          }
        });

        // all the answers having child nodes
        var childs = $(".child");
        var sameLevelThreshold = 3;
        $.each(childs, function(index, child) {
          var answers = $(child).children(".answercontainer");
          var showMoreElement = "<a class='showmore'>Show more replies [ " + (answers.length - sameLevelThreshold) + ((answers.length - sameLevelThreshold) > 1 ? " Children" : " Child") + " ]</a>";
          if (answers.length > sameLevelThreshold) {
            $(child).append($(showMoreElement));
            $.each(answers, function(index, answer) {
              if (index > sameLevelThreshold - 1) {
                answer.style.display = "none";
              }
            })
          }
        });

        // Temporary method to show the Posts
        // A url should replace soon
        $(".showmore").on("click", function(e) {
          e.preventDefault();
          $(this).siblings(".answercontainer").show();
          $(this).hide();
        })

        $(".minimise").on("click", function(e) {
          e.preventDefault();
          var nodeId = $(this).data("id"),
            $anchor = $(this).children("a"),
            $voteParent = $("#voteparent" + nodeId),
            $childVoteParent = $("#childVoteParent" + nodeId),
            $ansDesc = $("#answerdesc" + nodeId),
            $ans = $(this).closest(".answer");

          if ($anchor.text() == "[-]") {
            $ansDesc.hide();
            $ans.css("padding-top", "0px");
            if ($voteParent.css("display") == "block") {
              $voteParent.hide();
              $(this).data("parent", 1);
            }
            $anchor.text("[+]");
          } else if ($anchor.text() == "[+]") {
            $ansDesc.show();
            $ans.css("padding-top", "7px");
            if ($(this).data("parent")) {
              $voteParent.show();
            }
            $anchor.text("[-]");
          }
        })

        $(".textarea-reply").hide();
        $(".reply-submit").hide();
        $(".reply").on("click", function() {
          var textarea = $(this).siblings(".textarea-reply");
          var replysubmit = $(this).siblings(".reply-submit");
          if (textarea.css("display") == "none") {
            $(".textarea-reply").fadeOut(100);
            $(".reply-submit").fadeOut(100);
            textarea.fadeIn(100);
            replysubmit.fadeIn(100);
            $(this).text("Close");
          } else {
            textarea.fadeOut(100);
            replysubmit.fadeOut(100);
            $(this).text("Reply")
          }
        });
