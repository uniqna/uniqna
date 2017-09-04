var nav = new Vue({
  el: '.nav',
  data: {
    isActive: false,
    notification: `<i class="material-icons">notifications</i>`
  },
  methods: {
    toggleNav: function() {
      this.isActive = !this.isActive;
      if(this.isActive) {
        this.notification = 'Notifications';
      }
      else {
        this.notification = `<i class="material-icons">notifications</i>`;
      }
    }
  }
});

$(".post").click(function(){
    $(".modal-nav").addClass("is-active");
});

$(".modal-close").click(function(){
    $(".modal-nav").removeClass("is-active");
});

$(".modal-background").click(function(){
    $(".modal-nav").removeClass("is-active");
});

var search = false;
$(".search-icon").on("click", function(){
  if(search) {
    search = false;
    $("#search")
      .removeClass("rotate-in")
      .addClass("rotate-out")
      .text("search");
    $(".site-content")
      .removeClass("pull-down")
      .addClass("pull-up");
  }
  else {
    search = true;
    $("#search")
      .removeClass("rotate-out")
      .addClass("rotate-in")
      .text("close");
    $(".site-content")
      .removeClass("pull-up")
      .addClass("pull-down");
  }
});