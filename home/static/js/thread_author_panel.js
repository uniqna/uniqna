var overlay = new Vue({
  delimiters: ["[", "]"],
  el: '.author-panel',
  data: {
    bgcolor: '',
    content: '',
  }
});

var jargon = new Vue({
  el: '.level',
  methods: {
    changeText: function(dingdong) {
      if (dingdong == 'solved') {
        overlay.bgcolor = 'rgba(30, 215, 96, 0.9)';
        overlay.content= `<h1 class="title is-white">Yayy mark it as solved!</h1>
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
        overlay.bgcolor = 'rgba(198, 40, 40, 0.9)';
        overlay.content = `<h1 class="title is-white">Are you sure?</h1>
                          <h2 class="subtitle is-white" style="margin-bottom: 5px;">
                            This cannot be undone btw...
                          </h2>
                          <a class="button is-success" href="{% url 'delete_post' post.pk %}">
                            Yeup!
                          </a>`;
      }
        else if (dingdong == 'edit') {
        overlay.bgcolor = 'rgba(50, 115, 220, 0.9)';
        overlay.content = `
                          <div class="box">
                            WIP
                          </div>`;
      }
    }
  }
});

$(".trash").click(function() {
  $(".author-panel").addClass("is-active");
});

$(".edit").click(function() {
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
