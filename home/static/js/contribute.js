$(".contribute").click(function(){
    $(".contribute-modal").addClass("is-active");
});

$(".modal-close").click(function() {
  $(".contribute-modal").removeClass("is-active");
});

$(".modal-background").click(function() {
  $(".contribute-modal").removeClass("is-active");
});
