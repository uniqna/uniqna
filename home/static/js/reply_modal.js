var reply = new Vue({
  delimiters: ["[", "]"],
  el: '.replying-to',
  data: {
    username: '',
  }
});

var getuser = new Vue({
  el: '.reply-vue',
  methods: {
    giveUsername: function (dingdong) {
      reply.username = dingdong;
      $(".reply-modal").addClass("is-active");
    }
  }
});

$(".modal-close").click(function() {
  $(".reply-modal").removeClass("is-active");
});

$(".modal-background").click(function() {
  $(".reply-modal").removeClass("is-active");
});
