var reply = new Vue({
  delimiters: ["[", "]"],
  el: '.replying',
  data: {
    username: '',
    url: '',
  }
});

new Vue({
  el: '.reply-vue',
  methods: {
    getUserAndUrl: function(dingdong, reply_id) {
      reply.username = dingdong;
      var reply_url = window.location.origin + '/thread/reply/';
      reply.url = reply_url + reply_id + '/';
      $(".reply-modal").addClass("is-active");
    },
    getDeleteUrl: function(thread_id, reply_id) {
      replyAuthorModal.bgcolor = 'rgba(198, 40, 40, 0.9)';
      var delete_reply_url = window.location.origin + '/thread/' + thread_id + '/delete/answer/';
      replyAuthorModal.url = delete_reply_url + reply_id + '/';
    }
  }
});

var replyAuthorModal = new Vue({
  delimiters: ["[", "]"],
  el: '.reply-author-panel',
  data: {
    bgcolor: '',
    content: '',
    url: '',
  }
});

$(".modal-close").click(function() {
  $(".reply-modal").removeClass("is-active");
});

$(".modal-background").click(function() {
  $(".reply-modal").removeClass("is-active");
});

$(".reply-delete").click(function() {
  $(".reply-author-panel").addClass("is-active");
});

$(".modal-close").click(function() {
  $(".reply-author-panel").removeClass("is-active");
});

$(".modal-background").click(function() {
  $(".reply-author-panel").removeClass("is-active");
});
