// Voting script


(function(){

    $(".page-content").on('click', '.upvote', function() {
        vote_url = $(this).data("url");
        id = $(this).data("id");
        $.get(vote_url, function(data, status) {
            $("#up" + id).toggleClass("vote-default").toggleClass("vote-success");
            $("#down" + id).removeClass("vote-danger").addClass("vote-default")
            $("#score" + id).children()[0].textContent = data.points;
        });
    });

    $(".page-content").on('click', '.downvote', function() {
        vote_url = $(this).data("url");
        id = $(this).data("id");
        $.get(vote_url, function(data, status) {
            $("#down" + id).toggleClass("vote-default").toggleClass("vote-danger");
            $("#up" + id).removeClass("vote-success").addClass("vote-default");
            $("#score" + id).children()[0].textContent = data.points;
        });
    });

})();

