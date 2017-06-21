var reply_url = window.location.origin + '/thread/reply/';

var reply = new Vue({
  delimiters: ["[", "]"],
  el: '.replying',
  data: {
    username: '',
    url: '',
  }
});

var getuser = new Vue({
  el: '.reply-vue',
  methods: {
    giveUsername: function (dingdong, id) {
      reply.username = dingdong;
      reply.url = reply_url + id + '/';
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
