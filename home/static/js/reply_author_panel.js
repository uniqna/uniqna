var replyAuthorModal = new Vue({
  delimiters: ["[", "]"],
  el: '.reply-author-panel',
  data: {
    bgcolor: '',
    content: '',
  }
});

var replyAuthor = new Vue({
  el: '.content',
  methods: {
    changeText: function(dingdong) {
      if (dingdong == 'edit') {
        replyAuthorModal.bgcolor = 'rgba(30, 215, 96, 0.9)';
        replyAuthorModal.content= `<h1 class="title is-white">Yayy mark it as solved!</h1>
                            <h2 class="subtitle is-white" style="margin-bottom: 5px;">
                              Marking your question as solved is not mandatory;
                              do not feel compelled to accept the
                              first answer you receive.
                              Wait until you receive an answer
                              that answers your question well.
                            </h2>
                            <a class="button is-success" href="{% url 'mark_answer_solved' post.pk %}">
                              It\'s solved :D!
                            </a>`;
      } else if (dingdong == 'delete') {
        replyAuthorModal.bgcolor = 'rgba(198, 40, 40, 0.9)';
        replyAuthorModal.content = `<h1 class="title is-white">Are you sure?</h1>
                          <h2 class="subtitle is-white" style="margin-bottom: 5px;">
                            This cannot be undone btw...
                          </h2>
                          <a class="button is-success" href="{% url 'delete_post' post.pk %}">
                            Yeup!
                          </a>`;
      }
    }
  }
});

$(".reply-delete").click(function() {
  $(".reply-author-panel").addClass("is-active");
});

$(".reply-edit").click(function() {
  $(".reply-author-panel").addClass("is-active");
});

$(".modal-close").click(function() {
  $(".author-panel").removeClass("is-active");
});

$(".modal-background").click(function() {
  $(".author-panel").removeClass("is-active");
});
