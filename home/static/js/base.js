var nav = new Vue({
  el: '.nav',
  data: {
    isActive: false
  },
  methods: {
    toggleNav: function() {
      this.isActive = !this.isActive;
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
