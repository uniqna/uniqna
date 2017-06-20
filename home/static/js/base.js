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
    $(".modal").addClass("is-active");
});

$(".modal-close").click(function(){
    $(".modal").removeClass("is-active");
});

$(".modal-background").click(function(){
    $(".modal").removeClass("is-active");
});
