var overlay = new Vue({
  delimiters: ["[", "]"],
  el: '.author-panel',
  data: {
    message: '',
    subtitle: '',
    bgcolor: '',
    button: '',
    url: '',
  }
});

var jargon = new Vue({
  el: '.level',
  methods: {
    changeText: function(dingdong) {
      if (dingdong == 'solved') {
        overlay.message = 'Yayy mark it as solved!';
        overlay.subtitle = `Marking your question as solved is not mandatory;
                            do not feel compelled to accept the
                            first answer you receive.
                            Wait until you receive an answer
                            that answers your question well.`;
        overlay.bgcolor = 'rgba(30, 215, 96, 0.9)';
        overlay.button = 'It\'s solved :D';
        overlay.url = "{% url 'mark_answer_solved' post.pk %}";
      } else if (dingdong == 'delete') {
        overlay.message = 'Are you sure?';
        overlay.subtitle = 'This cannot be undone btw...';
        overlay.bgcolor = 'rgba(198, 40, 40, 0.9)';
        overlay.button = 'Yeup!';
        overlay.url = "{% url 'delete_post' post.pk %}";
      }
    }
  }
});

$(".trash").click(function() {
  $(".author-panel").addClass("is-active");
});

$(".solved").click(function(){
  if(!$('.solved').is('[disabled=disabled]')) {
    $(".author-panel").addClass("is-active");
  }
});

$(".modal-close").click(function() {
  $(".author-panel").removeClass("is-active");
});

$(".modal-background").click(function() {
  $(".author-panel").removeClass("is-active");
});
