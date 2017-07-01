(function(){
    // Parent voting
    // Element pattern references

    var up = "#up";
    var down = "#down";
    var score = "#score";

    $(".site-content").on('click', '.upvote', function() {
        vote_url = $(this).data("url");
        id = $(this).data("id");
        $.get(vote_url, function(data, status) {
            $(up + id).toggleClass("vote-default").toggleClass("vote-success");
            $(down + id).removeClass("vote-danger").addClass("vote-default");
            $(score + id).text(data.points);
        });
    });

    $(".site-content").on('click', '.downvote', function() {
        vote_url = $(this).data("url");
        id = $(this).data("id");
        $.get(vote_url, function(data, status) {
            $(down + id).toggleClass("vote-default").toggleClass("vote-danger");
            $(up + id).removeClass("vote-success").addClass("vote-default");
            $(score + id).text(data.points);
        });
    });

})();

(function(){
    // Answer voting

    var ansup = "#ans-up";
    var ansdown = "#ans-down";
    var ansscore = "#ans-score";

    $(".site-content").on("click", ".ans-upvote", function() {
            console.log("upping");
            vote_url = $(this).data("url");
            id = $(this).data("id");
            $.get(vote_url, function(data, status) {
                $(ansup + id).toggleClass("vote-default").toggleClass("vote-success");
                $(ansdown + id).removeClass("vote-danger").addClass("vote-default");
                $(ansscore + id).text(data.points);
            });
        });

    $(".site-content").on("click", ".ans-downvote", function() {
            vote_url = $(this).data("url");
            id = $(this).data("id");
            $.get(vote_url, function(data, status) {
                $(ansdown + id).toggleClass("vote-default").toggleClass("vote-danger");
                $(ansup + id).removeClass("vote-success").addClass("vote-default");
                $(ansscore + id).text(data.points);
            });
        });

})();
