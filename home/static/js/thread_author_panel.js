var modal = new Vue({
  delimiters: ["[", "]"],
  el: '.author-panel-modal',
  data: {
    bgcolor: '',
    content: '',
    subtitle: '',
    button: '',
    url: '',
    toggleEdit: '',
  }
});

new Vue({
  el: '.level',
  data: {
    url: ''
  },
  methods: {
    changeText: function(dingdong, target_url) {
      if (dingdong == 'solved') {
        modal.bgcolor = 'rgba(30, 215, 96, 0.9)';
        modal.url = target_url
        modal.button = 'It\'s solved :D!';
        modal.content = 'Yayy mark it as solved!';
        modal.subtitle = 'Marking your question as solved is not mandatory; do not feel compelled to accept the first answer you receive. Wait until you receive an answer that answers your question well.';
        modal.toggleEdit = false;

      } else if (dingdong == 'delete') {
        modal.bgcolor = 'rgba(198, 40, 40, 0.9)';
        modal.url = target_url;
        modal.button = 'Yeup!';
        modal.content = 'Are you sure?';
        modal.subtitle = 'This cannot be undone btw...';
        modal.toggleEdit = false;
      }
        else if (dingdong == 'edit') {
        modal.bgcolor = 'rgba(50, 115, 220, 0.9)';
        modal.url = target_url;
        modal.content = 'Your post will be marked as edited*';
        modal.subtitle = 'Sorry, post titles cannot be edited. However, you can simply delete it and resubmit the post. The sooner you do this, the less likely you will lose any votes or comments';
        modal.button = 'Done';
        modal.toggleEdit = true;
      }
    }
  }
});

$(".trash").click(function() {
  $(".author-panel-modal").addClass("is-active");
});

$(".edit").click(function() {
  $(".author-panel-modal").addClass("is-active");
});

$(".solved").click(function(){
  if(!$('.solved').is('[disabled=disabled]')) {
    $(".author-panel-modal").addClass("is-active");
  }
});

$(".modal-close").click(function() {
  $(".author-panel-modal").removeClass("is-active");
});

$(".modal-background").click(function() {
  $(".author-panel-modal").removeClass("is-active");
});

$('field').on( 'change keyup keydown paste cut', 'textarea', function (){
    $(this).height(0).height(this.scrollHeight);
}).find( 'textarea' ).change();
